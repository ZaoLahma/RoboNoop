from ...core.runtime.task_base import TaskBase
from ..log.log import Log
from .core_messages import CapabilitiesReq
from .core_messages import CapabilitiesCfm
from .message_protocol import MessageProtocol
import struct
import socket

class ConnectionInfo:
    def __init__(self, connection, port_no):
        self.connection = connection
        self.port_no = port_no
        self.capabilities = []

    def set_capabilities(self, capabilities):
        self.capabilities = capabilities

class CommEndpoint(TaskBase):
    def __init__(self, protocols):
        TaskBase.__init__(self)
        self.protocols = protocols
        self.connection_infos = []
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

    def get_all_messages(self):
        return self.received_messages

    def send_message(self, message):
        self.messages_to_send.append(message)

    def publish_service(self, port_no):
        Log.log("publish_service with port_no {}".format(port_no))
        try:
            conn_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            conn_listener.bind(('', port_no))
            conn_listener.settimeout(0.01)
            self.conn_listeners.append(conn_listener)
        except Exception as e:
            Log.log("Exception when publishing service " + str(port_no) + ": " + str(e))
    
    def is_connected(self, port_no):
        for connection_info in self.connection_infos:
            if connection_info.port_no == port_no:
                return True
        return False

    def run(self):
        self.accept_connections()
        self.receive_messages()
        self.send_messages()

    def send_messages(self):
        for connection_info in self.connection_infos:
            if [] == connection_info.capabilities:
                self.send_message_to_connection(connection_info.connection, CapabilitiesReq())
            for message in self.messages_to_send:
                if message.get_msg_id() in connection_info.capabilities:
                    self.send_message_to_connection(connection_info.connection, message)
        self.messages_to_send = []

    def receive_messages(self):
        self.received_messages = []
        for connection_info in self.connection_infos:
            received_messages = self.receive_messages_for_conn(connection_info.connection)
            for message in received_messages:
                if message.get_msg_id() == CapabilitiesCfm.get_msg_id():
                    for capability in message.msg_ids:
                        if capability not in connection_info.capabilities:
                            connection_info.capabilities.append(capability)
                elif message.get_msg_id() == CapabilitiesReq.get_msg_id():
                    capabilities_cfm = CapabilitiesCfm(self.protocols)
                    self.send_message_to_connection(connection_info.connection, capabilities_cfm)

            self.received_messages.extend(received_messages)

    def accept_connections(self):
        for listener in self.conn_listeners:
            try:
                listener.listen(1)
                (connection, address) = listener.accept()
                connection.settimeout(0.01)
                connection_info = ConnectionInfo(connection, -1)
                self.connection_infos.append(connection_info)
                Log.log("Connected to by " + str(address) + "...")
                self.send_message_to_connection(connection, CapabilitiesReq())
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
            connection_info = ConnectionInfo(connection, port_no)
            self.connection_infos.append(connection_info)
            self.send_message_to_connection(connection_info.connection, CapabilitiesReq())

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
                if len(data) > 0:
                    continue
                else:
                    return None
            except ConnectionResetError:
                return None
            return bytearray(data)

    def receive_message(self, connection):
        message = None
        header = self.receive_data(connection, 2)
        if None != header:
            size = struct.unpack(">H", header[0:2])[0]
            data = self.receive_data(connection, size)
            if None != data:
                for protocol in self.protocols:
                    message = protocol.decode_message(data)
                    if None != message:
                        break
        return message

    def send_message_to_connection(self, connection, message):
        data = MessageProtocol.encode_message(message)
        data_size = struct.pack(">H", len(data))
        connection.sendall(data_size)
        connection.sendall(data)