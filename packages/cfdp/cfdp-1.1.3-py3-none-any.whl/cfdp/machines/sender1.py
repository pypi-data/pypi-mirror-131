from cfdp import logger
from cfdp.constants import MachineState, ConditionCode, TransmissionMode,\
    Direction
from cfdp.event import EventType
from cfdp.pdu import MetadataPdu, FiledataPdu, EofPdu
from .base import Machine


class Sender1(Machine):

    """Implementation of Class 1 (unacknowledged transfer) sender."""

    def __init__(self, kernel, transaction):
        super().__init__(kernel, transaction)
        self.transmission_mode = TransmissionMode.UNACKNOWLEDGED
        self.state = MachineState.SEND_METADATA

    def update_state(self, event, pdu=None):
        """ See state table given in CCSDS 720.2-G-3, Table 5-1 """
        logger.debug("[{}] Event: {}".format(event.transaction.id, event.type))

        if self.state == MachineState.SEND_METADATA:

            if event.type == EventType.E0_ENTERED_STATE:
                self._initialize()

            elif event.type == EventType.E30_RECEIVED_PUT_REQUEST:
                self._issue_transaction_indication()
                self._send_metadata()
                if self._is_file_transfer():
                    self.state = MachineState.SEND_FILE
                    self.trigger_event(EventType.E0_ENTERED_STATE)
                else:
                    self._send_eof()
                    self._issue_eof_sent_indication()
                    self._issue_transaction_finished_indication()
                    self._shutdown()

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

        elif self.state == MachineState.SEND_FILE:

            if event.type == EventType.E0_ENTERED_STATE:
                self._open_source_file()
                self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E1_SEND_FILE_DATA:
                if not self.suspended and not self.frozen:
                    if self._is_comm_layer_ready():
                        self._send_file_data()
                        if self._is_entire_file_sent():
                            self._send_eof()
                            self._issue_eof_sent_indication()
                            self._issue_transaction_finished_indication()
                            self._shutdown()
                            return  # stop here
                    self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E2_ABANDON_TRANSACTION:
                self._issue_abandoned_indication()
                self._shutdown()

            elif event.type == EventType.E3_NOTICE_OF_CANCELLATION:
                self._send_eof()
                self._issue_transaction_finished_indication()
                self._shutdown()

            elif event.type == EventType.E4_NOTICE_OF_SUSPENSION:
                if not self.suspended:
                    self._issue_suspended_indication()
                    self.suspended = True

            elif event.type == EventType.E31_RECEIVED_SUSPEND_REQUEST:
                self.trigger_event(EventType.E4_NOTICE_OF_SUSPENSION)

            elif event.type == EventType.E32_RECEIVED_RESUME_REQUEST:
                if self.suspended:
                    self._issue_resumed_indication()
                    self.suspended = False
                    if not self.frozen:
                        self.trigger_event(EventType.E1_SEND_FILE_DATA)

            elif event.type == EventType.E33_RECEIVED_CANCEL_REQUEST:
                self.condition_code = ConditionCode.CANCEL_REQUEST_RECEIVED
                self.trigger_event(EventType.E3_NOTICE_OF_CANCELLATION)

            elif event.type == EventType.E34_RECEIVED_REPORT_REQUEST:
                self._issue_report_indication()

            elif event.type == EventType.E40_RECEIVED_FREEZE:
                self.frozen = True

            elif event.type == EventType.E41_RECEIVED_THAW:
                if self.frozen:
                    self.frozen = False
                    if not self.suspended:
                        self.trigger_event(EventType.E1_SEND_FILE_DATA)

            else:
                logger.debug(
                    "[{}] Event: {} not applicable for this state: {}"
                    .format(self.transaction.id, event.type, self.state))

    def _send_metadata(self):
        logger.debug("[{}] Send Metadata".format(self.transaction.id))
        pdu = MetadataPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            file_size=self.transaction.get_file_size(),
            source_filename=self.transaction.source_filename,
            destination_filename=self.transaction.destination_filename,
            filestore_requests=self.transaction.filestore_requests,
            messages_to_user=self.transaction.messages_to_user)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.encode(), address)

    def _send_file_data(self):
        logger.debug("[{}] Send Filedata".format(self.transaction.id))
        offset, data = self.transaction.get_file_segment()
        pdu = FiledataPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            segment_offset=offset,
            file_data=data)
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.encode(), address)

    def _send_eof(self):
        logger.debug("[{}] Send EOF".format(self.transaction.id))
        pdu = EofPdu(
            direction=Direction.TOWARD_RECEIVER,
            transmission_mode=self.transmission_mode,
            source_entity_id=self.transaction.source_entity_id,
            transaction_seq_number=self.transaction.seq_number,
            destination_entity_id=self.transaction.destination_entity_id,
            condition_code=self.condition_code,
            file_checksum=self.transaction.get_file_checksum(),
            file_size=self.transaction.get_file_size())
        address = self.kernel.config.get(
            self.transaction.destination_entity_id).ut_address
        self.kernel.transport.request(pdu.encode(), address)
