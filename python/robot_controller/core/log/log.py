from datetime import datetime
import inspect
import os

class Log:
    log_application_name = None
    log_file_name = "default_log_name.log"
    log_write_to_file = False

    @staticmethod
    def log(msg):
        now = datetime.now()
        frame = inspect.stack()[1]
        file_name = frame[0].f_code.co_filename
        line_no = frame[0].f_lineno
        file_name = str(file_name).split(os.path.sep)[-1]
        log_str = str(now) + " " 
        if None != Log.log_application_name:
            log_str += Log.log_application_name + " " 
        log_str += file_name + ":" + str(line_no) + " - " + str(msg)
        print(log_str)
        if Log.log_write_to_file:
            with open(Log.log_file_name, "a") as log_file:
                log_file.write(log_str + '\n')