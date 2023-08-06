import socket
import threading
import select

from . import Transport


DEFAULT_BUFFER_SIZE = 4096


class UdpTransport(Transport):

    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._incoming_pdu_thread = threading.Thread(
            target=self._incoming_pdu_handler)
        self._incoming_pdu_thread.kill = False

    def request(self, data, address):
        # address expected in the format "host:port"
        url = address.split(":")
        url[1] = int(url[1])
        self.socket.sendto(data, tuple(url))

    def bind(self):
        url = self.config.local_entity.ut_address
        url = url.split(":")
        url[1] = int(url[1])
        self.socket.bind(tuple(url))
        self._incoming_pdu_thread.start()

    def unbind(self):
        self._incoming_pdu_thread.kill = True
        self._incoming_pdu_thread.join()
        self.socket.close()

    def _incoming_pdu_handler(self):
        thread = threading.currentThread()
        _socket_list = [self.socket]

        # make sure that even the larges PDU will fit into the buffer
        maximum_file_segment_lengths = [
            self.config.get(x.entity_id).maximum_file_segment_length
            for x in self.config.remote_entities]
        if maximum_file_segment_lengths:
            buffer_size = 10 * max(maximum_file_segment_lengths)
        else:
            buffer_size = 10 * DEFAULT_BUFFER_SIZE

        while not thread.kill:
            try:
                readable, _, _ = select.select(_socket_list, [], [], 0)
            except ValueError:
                break

            for sock in readable:
                data, addr = sock.recvfrom(buffer_size)
                self.indication(data)
