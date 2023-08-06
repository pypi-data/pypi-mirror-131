from cfdp import logger
from cfdp.constants import MachineState, TransmissionMode, DeliveryCode,\
    ConditionCode
from cfdp.event import EventType
from cfdp.meta import execute_filestore_requests
from .timer import Timer
from .base import Machine


class Receiver1(Machine):

    """Implementation of Class 1 (unacknowledged transfer) receiver."""

    def __init__(self, kernel, transaction):
        super().__init__(kernel, transaction)
        self.transmission_mode = TransmissionMode.UNACKNOWLEDGED
        self.state = MachineState.WAIT_FOR_MD

        # inactivity timer
        timeout = kernel.config.get(
            transaction.source_entity_id).transaction_inactivity_limit
        self.inactivity_timer = Timer(
            self, timeout, EventType.E27_INACTIVITY_TIMEOUT)

    def update_state(self, event, pdu=None):
        """ See state table given in CCSDS 720.2-G-3, Table 5-2 """
        logger.debug("[{}] Event: {}".format(self.transaction.id, event.type))

        if pdu:
            self._restart_inactivity_timer()  # as per CCSDS 720.2-G-3, 5.3.7

        if self.state == MachineState.WAIT_FOR_MD:

            if event.type == EventType.E0_ENTERED_STATE:
                self._initialize()
                self._restart_inactivity_timer()

            elif event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E3_NOTICE_OF_CANCELLATION:
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E10_RECEIVED_METADATA:
                self._issue_metadata_received_indication(pdu.file_size)
                if self._is_file_transfer():
                    self._open_temp_file()
                self._process_metadata_options(pdu)
                self.state = MachineState.WAIT_FOR_EOF

            elif event.type == EventType.E12_RECEIVED_EOF_NO_ERROR:
                logger.info(
                    "[{}] Finished without Metadata received"
                    .format(self.transaction.id))
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self.condition_code = pdu.condition_code
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E27_INACTIVITY_TIMEOUT:
                self._restart_inactivity_timer()
                self._fault_inactivity()

            elif event.type == EventType.E33_RECEIVED_CANCEL_REQUEST:
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self.trigger_event(EventType.E3_NOTICE_OF_CANCELLATION)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

        elif self.state == MachineState.WAIT_FOR_EOF:

            if event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E3_NOTICE_OF_CANCELLATION:
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E11_RECEIVED_FILEDATA:
                self._issue_filesegment_received_indication(
                    pdu.segment_offset, len(pdu.file_data))
                if self._is_file_transfer():
                    self._store_file_data(pdu)
                    self._update_received_file_size(pdu)

            elif event.type == EventType.E12_RECEIVED_EOF_NO_ERROR:
                self._issue_eof_received_indication()

                if self._is_file_transfer():
                    if self._is_file_size_error(pdu.file_size):
                        self._fault_file_size()
                    if self._is_file_checksum_failure(pdu.file_checksum):
                        self._fault_file_checksum()

                    self.delivery_code = DeliveryCode.DATA_COMPLETE
                    self._copy_temp_file_to_dest_file()
                    self._close_temp_file()

                if self.transaction.filestore_requests:
                    execute_filestore_requests(
                        self.kernel, self.transaction.filestore_requests)

                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E13_RECEIVED_EOF_CANCEL:
                self.condition_code = pdu.condition_code
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E27_INACTIVITY_TIMEOUT:
                self._restart_inactivity_timer()
                self._fault_inactivity()

            elif event.type == EventType.E33_RECEIVED_CANCEL_REQUEST:
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self.trigger_event(EventType.E3_NOTICE_OF_CANCELLATION)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

    def _shutdown(self):
        super()._shutdown()
        self.inactivity_timer.shutdown()
