from ...core.runtime.task_base import TaskBase
from ..log.log import Log
from .core_messages import CapabilitiesReq
from .core_messages import CapabilitiesCfm
from .message_protocol import MessageProtocol
import struct
import socket

class ConnectionInfo:
    def __init__(self, connection):
        self.connection = connection
        self.capabilities = []

    def set_capabilities(self, capabilities):
        self.capabilities = capabilities


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
            received_messages = self.receive_messages_for_conn(connection)
            for message in received_messages:
                if message.get_msg_id() == CapabilitiesCfm.get_msg_id():
                    Log.log("Received capabilities " + str(message.msg_ids))
                    received_messages.remove(message)
                elif message.get_msg_id() == CapabilitiesReq.get_msg_id():
                    Log.log("Received capabilities req")
                    capabilities_cfm = CapabilitiesCfm(self.protocols)
                    self.send_message(connection, capabilities_cfm)

            self.received_messages.extend(received_messages)

    def accept_connections(self):
        for listener in self.conn_listeners:
            try:
                listener.listen(1)
                (connection, address) = listener.accept()
                connection.settimeout(0.01)
                self.connections.append(connection)
                Log.log("Connected to by " + str(address) + "...")
                self.send_message(connection, CapabilitiesReq())
            except socket.timeout:
                pass

    def connect(self, address, port_no):
        host = (address, port_no)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(0.01)
        try:
            connection.connect(host)
        except:
            raise
        else:
            Log.log("Connected to application at address {0}".format(host))
            self.connections.append(connection)

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
        if None != header:
            data_size = header[0:header_size]
            data_size = struct.unpack("<L", data_size)[0]
            data = self.receive_data(connection, data_size)
            if None != data:
                for protocol in self.protocols:
                    message = protocol.decode_message(data)
                    if None != message:
                        break
        return message
            

    def send_message(self, connection, message):
        Log.log("Sending message " + str(message) + "...")
        data = MessageProtocol.encode_message(message)
        Log.log("len data " + str(len(data)))
        data_size = (len(data)).to_bytes(4, byteorder='big')
        Log.log("data_size at send " + str(data_size))
        connection.sendall(data_size)
        connection.sendall(data)