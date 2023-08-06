import threading
import time
import zmq

from . import Transport
from .. import logger


class ZmqTransport(Transport):

    def __init__(self):
        super().__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)

        self._incoming_pdu_thread = threading.Thread(
            target=self._incoming_pdu_handler)
        self._incoming_pdu_thread.kill = False

    def request(self, data, address):
        self.socket.send(data)

    def connect(self, remote_entity_id):
        url = self.config.get(remote_entity_id).ut_address
        if url is None:
            logger.warning(
                "Remote entity %s id not configured" % remote_entity_id)
        else:
            self.socket.connect("tcp://{}".format(url))

    def disconnect(self):
        self.socket.close()

    def bind(self):
        url = self.config.local_entity.ut_address
        self.socket.bind("tcp://{}".format(url))
        self._incoming_pdu_thread.start()

    def unbind(self):
        self._incoming_pdu_thread.kill = True
        self._incoming_pdu_thread.join()

    def _incoming_pdu_handler(self):
        thread = threading.currentThread()
        while not thread.kill:
            time.sleep(0.01)
            try:
                # check if pdu was received, then send it to upper layer
                pdu = self.socket.recv(flags=zmq.NOBLOCK)
                self.indication(pdu)
            except zmq.Again:
                pass
            except zmq.ZMQError:
                break

    def shutdown(self):
        self.context.destroy()
