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
        Log.log("send_message called " + str(message))
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
            Log.log("Looking at connection info " + str(connection_info) + " that handles {}".format(connection_info.capabilities))
            for message in self.messages_to_send:
                Log.log("Number of connections {}".format(len(self.connection_infos)))
                if message.get_msg_id() in connection_info.capabilities:
                    Log.log("Found connection that handles {}".format(message.get_msg_id()))
                    self.send_message_to_connection(connection_info.connection, message)
        self.messages_to_send = []

    def receive_messages(self):
        self.received_messages = []
        for connection_info in self.connection_infos:
            Log.log("Receive messages for connection_info " + str(connection_info))
            received_messages = self.receive_messages_for_conn(connection_info.connection)
            for message in received_messages:
                if message.get_msg_id() == CapabilitiesCfm.get_msg_id():
                    Log.log("Received capabilities " + str(message.msg_ids))
                    for capability in message.msg_ids:
                        if capability not in connection_info.capabilities:
                            Log.log("Appended capability {} to connection ".format(capability) + str(connection_info))
                            connection_info.capabilities.append(capability)
                            Log.log("Appended to " + str(connection_info))
                elif message.get_msg_id() == CapabilitiesReq.get_msg_id():
                    Log.log("Received capabilities req")
                    capabilities_cfm = CapabilitiesCfm(self.protocols)
                    self.send_message_to_connection(connection_info.connection, capabilities_cfm)

            self.received_messages.extend(received_messages)

        Log.log("Connection infos after " + str(self.connection_infos))

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
            self.send_message_to_connection(connection, CapabilitiesReq())

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

    def send_message_to_connection(self, connection, message):
        Log.log("Sending message " + str(message) + "...")
        data = MessageProtocol.encode_message(message)
        Log.log("len data " + str(len(data)))
        data_size = (len(data)).to_bytes(4, byteorder='big')
        Log.log("data_size at send " + str(data_size))
        connection.sendall(data_size)
        connection.sendall(data)