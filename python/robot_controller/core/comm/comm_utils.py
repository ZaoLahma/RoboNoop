from ..log.log import Log
from ..config.config import Config

class CommUtils:
    @staticmethod
    def publish_service(comm_if, app_name):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"][app_name]["port-no"]
        comm_if.publish_service(port_no)

    @staticmethod
    def connect(comm_if, app_name):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"][app_name]["port-no"]
        host = app_config["comm"][app_name]["address"]

        ret_val = False
        if False == comm_if.is_connected(port_no):
            try:
                comm_if.connect(host, port_no)
                ret_val = True
            except Exception as e:
                try:
                    comm_if.connect("localhost", port_no)
                    ret_val = True
                except Exception as e:
                    Log.log("Exception when connecting to {0} at {1}:{2} - {3}".format(app_name, host, port_no, str(e)))
        else:
            ret_val = True
        return ret_val

    @staticmethod
    def is_connected(comm_if, app_name):
        app_config = Config.get_config_val("application")
        port_no = app_config["comm"][app_name]["port-no"]
        return comm_if.is_connected(port_no)