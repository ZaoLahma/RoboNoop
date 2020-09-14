from ..log.log import Log
import json

class Config():
    CONFIG_FILE_PATH = None
    def __init__(self, file_path):
        Log.log("Initiating config...")
        Config.CONFIG_FILE_PATH = file_path

    @staticmethod
    def read_config():
        config = None
        with open(Config.CONFIG_FILE_PATH) as json_file:
            config = json.load(json_file)
        return config

    @staticmethod
    def get_config_val(config_key):
        config = Config.read_config()
        return config[config_key]