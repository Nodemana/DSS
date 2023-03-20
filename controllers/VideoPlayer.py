import sys
import os
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QGuiApplication, QPainter, QImage
from PyQt5.QtCore import Qt, QTimer

class VideoPlayer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Video Player')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 800, 600)

        self.playlist_file = "../files/playlist.txt"
        self.load_playlist(self.playlist_file)

        self.show()

    def load_playlist(self, playlist_file):
        if os.path.exists(playlist_file):
            with open(playlist_file, 'r') as file:
                playlist_paths = [os.path.join('../files', line.strip()) for line in file.readlines()]

            screen = QApplication.desktop().screenGeometry()
            width = screen.width()
            height = screen.height()

            aspect_ratio = str(width) + ":" + str(height)
            self.instance = vlc.Instance("--autoscale")
            self.player = self.instance.media_player_new()
            self.player.video_set_aspect_ratio(aspect_ratio)
            self.media_list = self.instance.media_list_new(playlist_paths)
            self.media_list_player = self.instance.media_list_player_new()
            self.media_list_player.set_media_list(self.media_list)
            self.media_list_player.set_media_player(self.player)

            self.event_manager = self.player.event_manager()
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.video_end_callback)
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.video_error_callback)

            self.play_next_video()
        else:
            self.label.setText('Playlist file not found')

    def video_end_callback(self, event):
        self.play_next_video()

    def video_error_callback(self, event):
        print("Encountered an error while playing the video:")
        print(event.u.media_player_error)


    def play_next_video(self):
        if not self.media_list_player.is_playing():
            self.media_list_player.play()
            self.player.set_fullscreen(True)
            current_media = self.media_list_player.get_media_player().get_media()

    def run_video_player():
        app = QApplication(sys.argv)
        window = VideoPlayer()
        sys.exit(app.exec_())
    
