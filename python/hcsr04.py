from robot_controller.core.driver.hcsr04.main import Main
from robot_controller.core.config.config import Config
import sys
import getopt

if "__main__" == __name__:
    config_file = None

    if 2 == len(sys.argv):
        config_file = sys.argv[1]

    if None == config_file:
        print("Exiting")
        exit()
    else:
        Config.CONFIG_FILE_PATH = config_file
    
    Main.run()