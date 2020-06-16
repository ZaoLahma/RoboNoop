from ...core.runtime.task_base import TaskBase
from ..log.log import Log
from .core_messages import CapabilitiesReq
from .core_messages import CapabilitiesCfm
from .message_protocol import MessageProtocol
import struct
import socket

class CommEndpoint(TaskBase):
    def __init__(self, protocols):
        TaskBase.__init__(self)
        self.protocols = protocols
        self.connections = []
        self.conn_listeners = []
        self.messages_to_send = []
        self.received_messages = []

    def get_message(self, msg_id):
        ret_val = None
        for message in self.received_messages:
            if message.get_msg_id() == msg_id:
                ret_val = message
                break
        return ret_val

    def send_message(self, message):
        self.messages.append(message)

    def publish_service(self, port_no):
        conn_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn_listener.bind(('', port_no))
        conn_listener.settimeout(0.01)
        self.conn_listeners.append(conn_listener)

    def run(self):
        self.accept_connections()
        self.receive_messages()
        self.send_messages()

    def send_messages(self):
        # Broadcast for now. Should implement a capabilities check
        # in the protocol that states which messages are supported
        # by "the other" side
        for message in self.messages_to_send:
            for connection in self.connections:
                self.send_message(connection, message)
        self.messages_to_send = []

    def receive_messages(self):
        self.received_messages = []
        for connection in self.connections:
            self.received_messages.append(self.receive_messages_for_conn(connection))

    def accept_connections(self):
        for listener in self.conn_listeners:
            try:
                listener.listen(1)
                (connection, address) = listener.accept()
                self.connections.append(connection)
                Log.log("Connected to by " + str(address) + "...")
                self.send_message(connection, CapabilitiesReq())
            except socket.timeout:
                pass

    def receive_messages_for_conn(self, connection):
        messages = []
        message = self.receive_message(connection)
        while None != message:
            messages.append(message)
            message = self.receive_message(connection)
        
        return messages

    def receive_data(self, connection, num_bytes):
        data = []
        while (len(data) < num_bytes):
            try:
                packet = connection.recv(num_bytes - len(data))
                if not packet:
                    continue
                data += packet
            except socket.timeout:
                return None
            except ConnectionResetError:
                return None
            return bytearray(data)

    def receive_message(self, connection):
        message = None
        header_size = 4
        header = self.receive_data(connection, header_size)
        Log.log("Received data " + str(header))
        if None != header:
            data_size = bytearray(header[0:header_size])
            data_size = struct.unpack("<B", data_size)[0]
            data = self.receive_data(connection, data_size)
            if None != data:
                for protocol in self.protocols:
                    message = self.protocol.decode_message(data)
                    if None != message:
                        break
        return message
            

    def send_message(self, connection, message):
        Log.log("Sending message " + str(message) + "...")
        data = MessageProtocol.encode_message(message)
        data_size = (len(data)).to_bytes(4, byteorder='big')
        connection.sendall(data_size)
        connection.sendall(data)