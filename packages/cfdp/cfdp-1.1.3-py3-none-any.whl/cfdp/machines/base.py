from cfdp import logger
from cfdp.constants import MachineState, DeliveryCode, ConditionCode,\
    Direction, FileStatus, FaultHandlerAction
from cfdp.event import Event, EventType


class Machine:

    def __init__(self, kernel, transaction):
        self.kernel = kernel
        self.transaction = transaction

    def trigger_event(self, event_type):
        self.kernel.trigger_event(Event(self.transaction, event_type))

    def _initialize(self):
        # as per CCSDS 720.2-G-3, Page 5-13, g)
        self.condition_code = ConditionCode.NO_ERROR
        self.delivery_code = DeliveryCode.DATA_INCOMPLETE
        self.frozen = False
        self.metadata_received = False
        self.pdu_received = False
        self.suspended = False
        self.file_status = FileStatus.UNREPORTED
        self.filestore_responses = None
        self.status_report = None

        self.received_file_size = 0
        self.file_open = False
        self.received_file_segments = {}
        self.nak_list = []

    def _shutdown(self):
        if self.transaction.file_handle:
            self.transaction.file_handle.close()
            self.transaction.file_handle = None
        self.state = MachineState.COMPLETED

    def _issue_transaction_indication(self):
        self.kernel.transaction_indication(self.transaction.id)

    def _issue_eof_sent_indication(self):
        if self.kernel.config.get(self.kernel.entity_id).eof_sent_indication:
            self.kernel.eof_sent_indication(self.transaction.id)

    def _issue_transaction_finished_indication(self):
        if self.kernel.config.get(
                self.kernel.entity_id).transaction_finished_indication:
            self.kernel.transaction_finished_indication(
                self.transaction.id,
                self.condition_code,
                self.file_status,
                self.delivery_code,
                self.filestore_responses,
                self.status_report)

    def _issue_metadata_received_indication(self, file_size):
        self.kernel.metadata_received_indication(
            self.transaction.id,
            self.transaction.source_entity_id,
            file_size,
            self.transaction.source_filename,
            self.transaction.destination_filename,
            self.transaction.messages_to_user)

    def _issue_filesegment_received_indication(self, offset, length):
        if self.kernel.config.get(
                self.kernel.entity_id).file_segment_recv_indication:
            self.kernel.filesegment_received_indication(
                self.transaction.id,
                offset,
                length)

    def _issue_suspended_indication(self):
        if self.kernel.config.get(self.kernel.entity_id).suspended_indication:
            self.kernel.suspended_indication(
                self.transaction.id,
                self.condition_code)

    def _issue_resumed_indication(self):
        if self.kernel.config.get(self.kernel.entity_id).resumed_indication:
            self.kernel.resumed_indication(
                self.transaction.id,
                self.transaction.get_progress())

    def _issue_report_indication(self):
        self.kernel.report_indication(
            self.transaction.id,
            self.status_report)

    def _issue_abandoned_indication(self):
        self.kernel.abandoned_indication(
            self.transaction.id,
            self.condition_code,
            self.transaction.get_progress())

    def _issue_eof_received_indication(self):
        if self.kernel.config.get(self.kernel.entity_id).eof_recv_indication:
            self.kernel.eof_received_indication(self.transaction.id)

    def _fault_inactivity(self):
        logger.error(
            "[{}] Fault: Inactivity timeout".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.INACTIVITY_DETECTED)
        self._run_fault_handler(fault_handler)

    def _fault_filestore(self):
        logger.error(
            "[{}] Fault: Filestore".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.FILESTORE_REJECTION)
        self._run_fault_handler(fault_handler)

    def _fault_ack_limit(self):
        logger.error(
            "[{}] Fault: Ack limit".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.POSITIVE_ACK_LIMIT_REACHED)
        self._run_fault_handler(fault_handler)

    def _fault_file_size(self):
        logger.error(
            "[{}] Fault: File size".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.FILE_SIZE_ERROR)
        self._run_fault_handler(fault_handler)

    def _fault_file_checksum(self):
        logger.error(
            "[{}] Fault: File checksum".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.FILE_CHECKSUM_FAILURE)
        self._run_fault_handler(fault_handler)

    def _fault_nak_limit(self):
        logger.error(
            "[{}] Fault: Nak limit".format(self.transaction.id))
        fault_handler = self.transaction.get_fault_handler(
            ConditionCode.NAK_LIMIT_REACHED)
        self._run_fault_handler(fault_handler)

    def _run_fault_handler(self, fault_handler):
        if fault_handler == FaultHandlerAction.CANCEL:
            self.trigger_event(EventType.E33_RECEIVED_CANCEL_REQUEST)
        elif fault_handler == FaultHandlerAction.SUSPEND:
            self.trigger_event(EventType.E31_RECEIVED_SUSPEND_REQUEST)
        elif fault_handler == FaultHandlerAction.IGNORE:
            logger.info("Fault is being ignored. Continuing.")
        elif fault_handler == FaultHandlerAction.ABANDON:
            self.trigger_event(EventType.E2_ABANDON_TRANSACTION)
        else:
            raise ValueError

    def _open_source_file(self):
        if not self.kernel.filestore.is_file(self.transaction.source_filename):
            self._fault_filestore()
        self.transaction.file_handle =\
            self.kernel.filestore.open(self.transaction.source_filename)

    def _is_comm_layer_ready(self):
        return self.kernel.transport.is_ready()

    def _is_entire_file_sent(self):
        return self.transaction.is_file_send_complete()

    def _is_ack_limit_reached(self):
        return self.ack_timer.is_limit_reached()

    def _is_file_data_queued(self):
        if self.nak_list:
            return True
        else:
            return False

    def _queue_nakked_data(self, pdu):
        if pdu.segment_requests:
            self.nak_list.extend(pdu.segment_requests)
            self.nak_list = list(sorted(set(self.nak_list)))

    def _restart_inactivity_timer(self):
        if not self.suspended:
            self.inactivity_timer.restart()

    def _resume_inactivity_timer(self):
        if not self.suspended:
            self.inactivity_timer.restart()

    def _suspend_inactivity_timer(self):
        self.inactivity_timer.cancel()

    def _restart_ack_timer(self):
        self.ack_timer.restart()

    def _cancel_ack_timer(self):
        self.ack_timer.cancel()

    def _suspend_ack_timer(self):
        self.ack_timer.suspended = True
        self.ack_timer.stop()

    def _resume_ack_timer(self):
        self.ack_timer.suspended = False
        self._restart_ack_timer()

    def _open_temp_file(self):
        self.transaction.file_handle = self.kernel.filestore.open_tempfile()

    def _close_temp_file(self):
        self.transaction.file_handle.close()

    def _copy_temp_file_to_dest_file(self):
        fh = self.kernel.filestore.open(
            self.transaction.destination_filename, 'wb')
        self.transaction.file_handle.seek(0)
        fh.write(self.transaction.file_handle.read())
        fh.close()

    def _is_file_transfer(self):
        if self.transaction.source_filename is None\
                or len(self.transaction.source_filename) == 0:
            return False
        return True

    def _is_file_size_error(self, file_size):
        if self.received_file_size > file_size:
            return True
        else:
            return False

    def _is_file_checksum_failure(self, checksum):
        # calculate checksum from file handle directly,
        # as it may be a temporary file
        calculated_checksum = self.transaction.file_handle.calculate_checksum(
            self.transaction.checksum_type)
        if calculated_checksum != checksum:
            return True
        else:
            return False

    def _store_file_data(self, pdu):
        self.transaction.file_handle.seek(pdu.segment_offset)
        self.transaction.file_handle.write(pdu.file_data)
        self.received_file_segments[pdu.segment_offset] = len(pdu.file_data)

    def _update_received_file_size(self, pdu):
        if self.received_file_size < pdu.segment_offset + len(pdu.file_data):
            self.received_file_size = pdu.segment_offset + len(pdu.file_data)

    def _process_metadata_options(self, pdu):
        self.transaction.filestore_requests = pdu.filestore_requests
        self.transaction.messages_to_user = pdu.messages_to_user
        # process user messages
        for message in self.transaction.messages_to_user:
            message.originating_transaction = self.transaction
            self.kernel.messages_to_user.append(message)

    def _restart_nak_timer(self):
        self.nak_timer.restart()

    def _cancel_nak_timer(self):
        self.nak_timer.cancel()

    def _reuse_senders_first_pdu_header(self, pdu):
        # as per CCSDS 702.2-G-3, 5.6.1 l)
        if not self.pdu_received:
            self.pdu_received = True
            self.first_pdu_header = pdu.pdu_header
            # reverse the direction field
            if pdu.pdu_header.direction == Direction.TOWARD_RECEIVER:
                self.first_pdu_header.direction = Direction.TOWARD_SENDER
            else:
                self.first_pdu_header.direction = Direction.RECEIVER

    def _is_nak_list_empty(self):
        if self.nak_list:
            return False
        else:
            return True

    def _update_nak_list(self, event, file_size=None):
        self.nak_list = []
        pointer = 0
        if not self.metadata_received:
            self.nak_list.append((0, 0))
        for offset, length in sorted(self.received_file_segments.items()):
            if offset > pointer:
                self.nak_list.append((pointer, offset))
            pointer = offset + length
        if file_size is not None:
            if pointer < file_size:
                self.nak_list.append((pointer, file_size))

    def _get_segment_requests(self):
        return self.nak_list
