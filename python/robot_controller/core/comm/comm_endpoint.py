from ...core.runtime.task_base import TaskBase
from ..log.log import Log
from .message_protocol import MessageProtocol
USE_PSUTIL = True
try:
    import psutil
except ImportError:
    USE_PSUTIL = False
import struct
import socket

class ConnectionInfo:
    def __init__(self, connection, port_no):
        self.connection = connection
        self.port_no = port_no

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

    def invalidate_messages(self):
        self.received_messages = []

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
            for message in self.messages_to_send:
                if False == self.send_message_to_connection(connection_info.connection, message):
                    self.connection_infos.remove(connection_info)
                    break
        self.messages_to_send = []

    def receive_messages(self):
        self.received_messages = []
        for connection_info in self.connection_infos:
            received_messages = self.receive_messages_for_conn(connection_info.connection)
            if None != received_messages:
                if False == received_messages:
                    self.connection_infos.remove(connection_info)
                else:
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

    def receive_messages_for_conn(self, connection):
        messages = []
        message = self.receive_message(connection)
        while None != message:
            if False == message:
                return False
            messages.append(message)
            message = self.receive_message(connection)
        
        return messages

    def receive_data(self, connection, num_bytes):
        data = [None] * num_bytes
        data_index = 0
        while (data_index < num_bytes):
            try:
                packet = connection.recv(num_bytes - data_index)
                if not packet:
                    return False
                for byte in packet:
                    data[data_index] = byte
                    data_index = data_index + 1
            except socket.timeout:
                if data_index > 0:
                    continue
                else:
                    return None
            except ConnectionResetError:
                return None
            except MemoryError:
                Log.log("Out of memory, skipping message")
                if True == USE_PSUTIL:
                    Log.log(str(psutil.virtual_memory().available))
                return None
            try:
                return bytearray(data)
            except:
                Log.log("Failed to encode data")
                return None

    def receive_message(self, connection):
        message = None
        header = self.receive_data(connection, 4)
        if None != header:
            if False == header:
                return False
            size = struct.unpack(">i", header[0:4])[0]
            data = self.receive_data(connection, size)
            if None != data:
                if False == data:
                    return False
                for protocol in self.protocols:
                    message = protocol.decode_message(data)
                    if None != message:
                        break
        return message

    def send_message_to_connection(self, connection, message):
        data = MessageProtocol.encode_message(message)
        data_size = struct.pack(">i", len(data))
        try:
            connection.sendall(data_size)
            connection.sendall(data)
            return True
        except Exception:
            return False