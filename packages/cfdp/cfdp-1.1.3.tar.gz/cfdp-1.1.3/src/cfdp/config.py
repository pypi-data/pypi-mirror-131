from .constants import TransmissionMode, ProtocolVersion, ConditionCode,\
    FaultHandlerAction, ChecksumType


DEFAULT_MAX_FILE_SEGMENT_LEN = 4096
DEFAULT_INACTIVITY_TIMEOUT = 30
DEFAULT_ACK_TIMER_LIMIT = 5
DEFAULT_ACK_TIMER_EXPIRATION_LIMIT = 3
DEFAULT_NAK_TIMER_INTERVAL = 5
DEFAULT_NAK_TIMER_EXPIRATION_LIMIT = 5


class Config:

    def __init__(
            self, local_entity, filestore, transport, remote_entities=[]):
        self.local_entity = local_entity
        if not isinstance(remote_entities, list):
            self.remote_entities = [remote_entities]
        else:
            self.remote_entities = remote_entities
        self.filestore = filestore
        self.filestore.config = self
        self.transport = transport
        self.transport.config = self

    def get(self, entity_id):
        if entity_id == self.local_entity.entity_id:
            return self.local_entity
        else:
            for x in self.remote_entities:
                if x.entity_id == entity_id:
                    return x
            else:
                return DefaultConfig()


class DefaultConfig:

    transaction_inactivity_limit = DEFAULT_INACTIVITY_TIMEOUT
    fault_handlers = {
        ConditionCode.POSITIVE_ACK_LIMIT_REACHED: FaultHandlerAction.CANCEL,
        ConditionCode.KEEP_ALIVE_LIMIT_REACHED: FaultHandlerAction.CANCEL,
        ConditionCode.INVALID_TRANSMISSION_MODE: FaultHandlerAction.CANCEL,
        ConditionCode.FILESTORE_REJECTION: FaultHandlerAction.CANCEL,
        ConditionCode.FILE_CHECKSUM_FAILURE: FaultHandlerAction.CANCEL,
        ConditionCode.FILE_SIZE_ERROR: FaultHandlerAction.CANCEL,
        ConditionCode.NAK_LIMIT_REACHED: FaultHandlerAction.CANCEL,
        ConditionCode.INACTIVITY_DETECTED: FaultHandlerAction.CANCEL,
        ConditionCode.INVALID_FILE_STRUCTURE: FaultHandlerAction.CANCEL,
        ConditionCode.CHECK_LIMIT_REACHED: FaultHandlerAction.CANCEL,
        ConditionCode.UNSUPPORTED_CHECKSUM_TYPE: FaultHandlerAction.CANCEL,
    }


class LocalEntity:

    """ Configuration options as per Table 8-1 in CCSDS 727.0-B-5 """

    def __init__(
            self,
            entity_id,
            ut_address,
            eof_sent_indication=True,
            eof_recv_indication=True,
            file_segment_recv_indication=True,
            transaction_finished_indication=True,
            suspended_indication=True,
            resumed_indication=True,
            default_fault_handlers=DefaultConfig.fault_handlers):
        self.entity_id = entity_id
        self.ut_address = ut_address
        self.eof_sent_indication = eof_sent_indication
        self.eof_recv_indication = eof_recv_indication
        self.file_segment_recv_indication = file_segment_recv_indication
        self.transaction_finished_indication = transaction_finished_indication
        self.suspended_indication = suspended_indication
        self.resumed_indication = resumed_indication
        self.default_fault_handlers = default_fault_handlers

        self.maximum_file_segment_length = None


class RemoteEntity:

    """ Configuration options as per Table 8-2 in CCSDS 727.0-B-5 """

    def __init__(
            self,
            entity_id,
            ut_address,
            protocol_version_number=ProtocolVersion.VERSION_2,
            positive_ack_timer_interval=DEFAULT_ACK_TIMER_LIMIT,
            nak_timer_interval=DEFAULT_NAK_TIMER_INTERVAL,
            keep_alive_interval=None,
            immediate_nak_mode_enabled=False,
            default_transmission_mode=TransmissionMode.UNACKNOWLEDGED,
            transaction_closure_requested=False,
            check_limit=None,
            type_of_checksum=ChecksumType.MODULAR,
            disposition_choice=None,  # Not used. Discard incomplete files
            crc_required_on_transmission=False,
            maximum_file_segment_length=DEFAULT_MAX_FILE_SEGMENT_LEN,
            keep_alive_discrepancy_limit=None,
            positive_ack_timer_expiration_limit=DEFAULT_ACK_TIMER_EXPIRATION_LIMIT,
            nak_timer_expiration_limit=DEFAULT_NAK_TIMER_EXPIRATION_LIMIT,
            transaction_inactivity_limit=DEFAULT_INACTIVITY_TIMEOUT,
            start_of_transmission_opportunity=None,
            end_of_transmission_opportunity=None,
            start_of_reception_opportunity=None,
            end_of_reception_opportunity=None):

        self.entity_id = entity_id
        self.ut_address = ut_address
        self.protocol_version_number = protocol_version_number
        self.positive_ack_timer_interval = positive_ack_timer_interval
        self.nak_timer_interval = nak_timer_interval
        self.keep_alive_interval = keep_alive_interval
        self.immediate_nak_mode_enabled = immediate_nak_mode_enabled
        self.default_transmission_mode = default_transmission_mode
        self.transaction_closure_requested = transaction_closure_requested
        self.check_limit = check_limit
        self.type_of_checksum = type_of_checksum
        self.disposition_choice = disposition_choice
        self.crc_required_on_transmission = crc_required_on_transmission
        self.maximum_file_segment_length = maximum_file_segment_length
        self.keep_alive_discrepancy_limit = keep_alive_discrepancy_limit
        self.positive_ack_timer_expiration_limit = positive_ack_timer_expiration_limit
        self.nak_timer_expiration_limit = nak_timer_expiration_limit
        self.transaction_inactivity_limit = transaction_inactivity_limit
        self.start_of_transmission_opportunity = start_of_transmission_opportunity
        self.end_of_transmission_opportunity = end_of_transmission_opportunity
        self.start_of_reception_opportunity = start_of_reception_opportunity
        self.end_of_reception_opportunity = end_of_reception_opportunity
