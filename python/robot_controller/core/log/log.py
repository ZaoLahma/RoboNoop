from datetime import datetime

class Log:
    log_file_name = "default_log_name.log"
    log_write_to_file = False

    @staticmethod
    def log(msg):
        now = datetime.now()
        with open(Log.log_file_name, "a") as log_file:
            log_str = str(now) + " - " + msg
            print(log_str)
            if Log.log_write_to_file:
                log_file.write(log_str + '\n')