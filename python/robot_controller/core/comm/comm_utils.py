from ..log.log import Log

class CommUtils:
    @staticmethod
    def connect(comm_if, host, port_no, connection_name):
        ret_val = False
        if False == comm_if.is_connected(port_no):
            try:
                comm_if.connect(host, port_no)
                ret_val = True
            except Exception as e:
                Log.log("Exception when connecting to {0}: {1}".format(connection_name, str(e)))
        else:
            ret_val = True
        return ret_val