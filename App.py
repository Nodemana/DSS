from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from views.main_window import *
from controllers import ftp_controller
import threading
# Get the absolute path of the current file

def main():
    #ftp_controller.sync()
    run_gui()



if __name__ == '__main__':
    main()