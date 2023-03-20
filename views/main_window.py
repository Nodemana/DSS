from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import sys
from datetime import datetime, timedelta


# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'models' directory to the system path
models_dir = os.path.join(current_dir, '..', 'models')
sys.path.append(models_dir)

# Add the 'models' directory to the system path
models_dir = os.path.join(current_dir, '..', 'controllers')

sys.path.append(models_dir)

# Import the ftp_model module
from ftp_model import *
from ftp_controller import *
from VideoPlayer import *



class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setGeometry(2500, 50, 1000, 800)
        self.setWindowTitle("DSS")

        # Create title label
        self.title_label = QLabel(self)
        self.title_label.setText("DSS")
        self.title_label.setFont(QFont("Arial", 16))
        self.title_label.move(50, 0)

        # Create local files subtitle label
        self.local_files_label = QLabel(self)
        self.local_files_label.setText("Local Files")
        self.local_files_label.setFont(QFont("Arial", 14))
        self.local_files_label.move(50, 28)

        # Create remote files subtitle label
        self.remote_files_label = QLabel(self)
        self.remote_files_label.setText("Remote Files")
        self.remote_files_label.setFont(QFont("Arial", 14))
        self.remote_files_label.move(50, 328)

        # Create local video list widget
        self.local_video_list = QListWidget(self)
        self.local_video_list.setGeometry(50, 50, 800, 200)
        files = os.listdir("files/")
        for file in files:
            item = QListWidgetItem(file)
            mtime = os.path.getmtime("files/" + file)
            item.setData(1, mtime) # store the modification time in the item's data
            self.local_video_list.addItem(item)
            item.setText("{:<30} {}".format(file, self.format_date(mtime)))

        # Create remote video list widget
        self.remote_video_list = QListWidget(self)
        self.remote_video_list.setGeometry(50, 350, 800, 200)
        remote_files = grab_files()
        for file in remote_files:
            print(file)
            item = QListWidgetItem(file[0])
            item.setData(1, mtime) # store the modification time in the item's data
            self.remote_video_list.addItem(item)
            item.setText("{:<30} {}".format(file[0], self.format_date_remote(file[2])))

        # Create play button
        self.play_button = QPushButton(self)
        self.play_button.setText("play")
        self.play_button.setFont(QFont("Arial", 12))
        self.play_button.move(50, 300)
        self.delete_button.clicked.connect(self.play_button_press)

        # Create fetch button
        self.fetch_button = QPushButton(self)
        self.fetch_button.setText("fetch")
        self.fetch_button.setFont(QFont("Arial", 12))
        self.fetch_button.move(200, 300)
        # self.fetch_button.clicked.connect(fetch_button_press)

        # Create delete button
        self.delete_button = QPushButton(self)
        self.delete_button.setText("delete")
        self.delete_button.setFont(QFont("Arial", 12))
        self.delete_button.move(350, 300)
        self.delete_button.clicked.connect(self.delete_button_press)

    def delete_button_press(self):
        selected_item = self.local_video_list.currentItem()
        if selected_item:
            filename = selected_item.text().split()[0]
            filename = os.path.basename(os.path.join("../files", filename))
            os.remove(os.path.join("../files", filename))
            self.local_video_list.takeItem(self.local_video_list.row(selected_item))

    def play_button_press(self):
        run_video_player()
        
    def fetch_button_press(self):
        print("Fetch Button Sync")
        sync()
        print("Fetch Complete")

    def format_date(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def format_date_remote(self, timestamp):
        # Parse the input string to a datetime object
        dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S.%f')
        dt = dt + timedelta(hours = 10)
        # Format the datetime object as a string in the desired format
        return dt.strftime('%Y-%m-%d %H:%M:%S')

def run_gui():
    app = QApplication([])
    window = HomeWindow()
    window.show()
    app.exec_()