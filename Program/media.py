import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from ui_chromecaster import Ui_Chromecaster

class MediaFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_filename(self):
        return os.path.basename(self.file_path)

class VideoFile(MediaFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.content_type = "video/mp4"

    def play(self, play_media_func):
        play_media_func(self.get_filename())

class SubtitleFile(MediaFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.content_type = "text/srt"

    def get_subtitle_url(self):
        return f"http://din_server_ip:5000/subtitles/{self.get_filename()}"

class ChromecasterGUI(QMainWindow, Ui_Chromecaster):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.video_file = None
        self.subtitle_file = None
        
        self.btnVideo.clicked.connect(self.select_video_file)
        self.btnSRT.clicked.connect(self.select_subtitle_file)
        self.btnStart.clicked.connect(self.start_playback)

    def select_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Välj videofil", "", "Video Files (*.mp4)")
        if file_path:
            self.video_file = VideoFile(file_path)
            self.txtVideo.setText(self.video_file.get_filename())

    def select_subtitle_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Välj undertextsfil", "", "Subtitle Files (*.srt)")
        if file_path:
            self.subtitle_file = SubtitleFile(file_path)
            self.txtSRT.setText(self.subtitle_file.get_filename())

    def start_playback(self, play_media_func):
        if self.video_file:
            self.video_file.play(play_media_func)
            if self.subtitle_file:
                self.video_file.media_info["subtitle_url"] = self.subtitle_file.get_subtitle_url()