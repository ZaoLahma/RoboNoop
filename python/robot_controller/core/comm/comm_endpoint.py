from ...core.runtime.task_base import TaskBase
from ...core.comm.core_messages import CapabilitiesInd
from ..log.log import Log
from .message_protocol import MessageProtocol
from threading import Thread, Lock
import struct
import socket
import select


class ConnectionListener(Thread):
    def __init__(self, conn_established):
        Thread.__init__(self)
        self.conn_established = conn_established
        self.conn_listeners = []
        self.active = False

    def publish_service(self, port_no):
        conn_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn_listener.bind(('', port_no))
        conn_listener.listen(1)
        self.conn_listeners.append(conn_listener)

    def run(self):
        Log.log("Connection listener started")
        self.active = True
        while True == self.active:
            readable, _, exceptional = select.select(self.conn_listeners, [], self.conn_listeners, 1)
            for sock in readable:
                (connection, address) = sock.accept()
                Log.log("Connected to by {}".format(address))
                self.conn_established(sock.getsockname()[1], connection)

            for broken in exceptional:
                self.conn_listeners.remove(broken)

    def stop(self):
        self.active = False

class ConnectionHandler(Thread):
    def __init__(self, port_no, connection, protocols):
        Thread.__init__(self)
        self.port_no = port_no
        self.inputs = [connection]
        self.protocols = protocols
        self.outputs = []
        self.messages_to_send = {}
        self.received_messages = []
        self.peer_capabilities = []
        self.active = False
        self.send_mutex = Lock()
        self.receive_mutex = Lock()

    def send_messages(self, messages):
        for message in messages:
            self.send_message(message)

    def send_message(self, message):
        if CapabilitiesInd.get_msg_id() == message.get_msg_id() or message.get_msg_id() in self.peer_capabilities:
            self.send_mutex.acquire()
            self.messages_to_send[message.get_msg_id()] = message
            self.outputs = self.inputs
            self.send_mutex.release()

    def get_received_messages(self):
        self.receive_mutex.acquire()
        ret_val = self.received_messages
        self.received_messages = []
        self.receive_mutex.release()
        return ret_val

    def run(self):
        Log.log("ConnectionHandler started for {}".format(self.port_no))
        own_capabilities = []
        for protocol in self.protocols:
            for message_class in protocol.message_classes:
                own_capabilities.append(message_class.get_msg_id())
        Log.log("Sending capabilities: {}".format(own_capabilities))
        self.send_message(CapabilitiesInd(own_capabilities))
        self.active = True
        while True == self.active:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0.05)

            for broken_sock in exceptional:
                self.inputs.remove(broken_sock)

            for read_sock in readable:
                self.receive_next_message(read_sock)

            for write_sock in writable:
                self.send_messages_to_sock(write_sock)

        Log.log("Exiting ConnectionHandler for {}".format(self.port_no))

    def receive_next_message(self, read_sock):
        curr_messages = []
        read_sock.settimeout(0.1)
        message = self.receive_message(read_sock)
        if None != message:
            Log.log("message: " + str(message))
            if CapabilitiesInd.get_msg_id() == message.get_msg_id():
                self.peer_capabilities = message.capabilities
                Log.log("Received capabilities: {} ({})".format(self.peer_capabilities, self.port_no))
            else:
                curr_messages.append(message)
            message = self.receive_message(read_sock)
        read_sock.settimeout(None)
        self.receive_mutex.acquire()
        self.received_messages = curr_messages
        self.receive_mutex.release()

    def receive_message(self, read_sock):
        message = None
        header = self.receive_data(read_sock, 4)
        if None != header:
            if False == header:
                return False
            size = struct.unpack(">i", header[0:4])[0]
            data = self.receive_data(read_sock, size)
            if None != data:
                for protocol in self.protocols:
                    message = protocol.decode_message(data)
                    if None != message:
                        break
        return message

    def receive_data(self, read_sock, num_bytes):
        data = num_bytes * [None]
        num_received_bytes = 0
        while (num_received_bytes < num_bytes):
            try:
                packet = read_sock.recv(num_bytes - num_received_bytes)
                if not packet:
                    self.active = False
                    return None
                data[num_received_bytes : num_received_bytes + len(packet)] = packet
                num_received_bytes += len(packet)
            except socket.timeout:
                if num_received_bytes > 0:
                    continue
                else:
                    return None
            except ConnectionResetError:
                self.active = False
                return None
        return bytearray(data)

    def send_messages_to_sock(self, send_sock):
        self.send_mutex.acquire()
        curr_messages_to_send = self.messages_to_send.values()
        self.messages_to_send = {}
        self.send_mutex.release()
        for message in curr_messages_to_send:
            data = MessageProtocol.encode_message(message)
            data_size = struct.pack(">i", len(data))
            try:
                send_sock.sendall(data_size)
                send_sock.sendall(data)
            except Exception:
                self.active = False
                break
        self.outputs = []

    def stop(self):
        self.active = False


class CommEndpoint(TaskBase):
    def __init__(self, protocols):
        TaskBase.__init__(self)
        self.protocols = protocols
        self.conn_listener = ConnectionListener(self.conn_established)
        self.conn_listener.start()
        self.connection_handlers = []
        self.received_messages = []
        self.messages_to_send = []

    def conn_established(self, port_no, connection):
        Log.log("Callback for connection received {}".format(port_no))
        connection_handler = ConnectionHandler(port_no, connection, self.protocols)
        connection_handler.start()
        self.connection_handlers.append(connection_handler)

    def get_message(self, msg_id):
        ret_val = None
        #Log.log("Received messages: {0}".format(self.received_messages))
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
        self.conn_listener.publish_service(port_no)
    
    def is_connected(self, port_no):
        ret_val = False
        for connection_handler in self.connection_handlers:
            if connection_handler.port_no == port_no and True == connection_handler.active:
                ret_val = True
                break
        return ret_val

    def run(self):
        self.received_messages = []
        disconnected =  []
        for connection_handler in self.connection_handlers:
            messages = connection_handler.get_received_messages()
            self.received_messages.extend(messages)
            if True == connection_handler.active:
                connection_handler.send_messages(self.messages_to_send)
            else:
                disconnected.append(connection_handler)
        self.messages_to_send = []

        for broken in disconnected:
            Log.log("Disconnecting {}".format(broken.port_no))
            self.connection_handlers.remove(broken)

    def stop(self):
        Log.log("CommEndpoint stop called")
        self.conn_listener.stop()
        for connection_handler in self.connection_handlers:
            connection_handler.stop()

    def connect(self, address, port_no):
        host = (address, port_no)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection.settimeout(1)
            connection.connect(host)
        except:
            raise
        else:
            Log.log("Connected to application at address {0}".format(host))
            connection.settimeout(None)
            connection_handler = ConnectionHandler(port_no, connection, self.protocols)
            connection_handler.start()
            self.connection_handlers.append(connection_handler)