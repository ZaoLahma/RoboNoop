from robot_controller.applications.garrus.main import Main
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