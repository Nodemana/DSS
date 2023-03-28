from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from views.main_window import *
from controllers import ftp_controller
import threading
import traceback
# Get the absolute path of the current file

def main():
    try:
        ftp_controller.sync()
        run_gui()
    except Exception as e:
        traceback.print_exc()




if __name__ == '__main__':
    main()