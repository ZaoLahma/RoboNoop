from ...core.runtime.task_base import TaskBase
from ..log.log import Log
import struct
import socket

class CommEndpoint(TaskBase):
    def __init__(self, protocol):
        TaskBase.__init__(self)
        self.protocol = protocol
        self.connections = []
        self.message_receivers = []
        self.conn_listeners = []

    def register_message_receiver(self, message_receiver):
        self.message_receivers.add(message_receiver)

    def publish_service(self, port_no):
        conn_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn_listener.bind(('', port_no))
        conn_listener.settimeout(0.01)
        self.conn_listeners.append(conn_listener)

    def run(self):
        messages = []
        for listener in self.conn_listeners:
            try:
                listener.listen(1)
                (connection, address) = self.server_socket.accept()
                self.connections.append(connection)
            except socket.timeout:
                pass

        for connection in self.connections:
            messages.append(self.receive_messages(connection))
        
        # Broadcast for now. Should implement a capabilities check
        # in the protocol that states which messages are supported
        # by "the other" side
        for message in self.messages:
            for connection in self.connections:
                self.send_message(connection, message)

    def receive_messages(self, connection):
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
        if None != header:
            data_size = bytearray(header[0:header_size])
            data_size = struct.unpack("<B", data_size)[0]
            data = self.receive_data(connection, data_size)
            if None != data:
                message = self.protocol.decode_message(data)
        return message
            

    def send_message(self, connection, message):
        data = message.encode()
        data_size = (len(data)).to_bytes(4, byteorder='big')
        connection.sendall(data_size)
        connection.sendall(data)