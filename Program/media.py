import os
import threading
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from pychromecast import get_chromecasts
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
    # Definiera en signal för att uppdatera Chromecast-listan i ComboBox
    chromecast_found = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.video_file = None
        self.subtitle_file = None
        self.chromecasts = []  # Lagra hittade Chromecast-enheter

        # Koppla knapparna till funktioner
        self.btnVideo.clicked.connect(self.select_video_file)
        self.btnSRT.clicked.connect(self.select_subtitle_file)
        self.btnStart.clicked.connect(self.start_playback)
        self.btnSearchChromecast.clicked.connect(self.search_chromecast)

        # Anslut signalen till metoden som uppdaterar ComboBox
        self.chromecast_found.connect(self.update_chromecast_combo)

    def search_chromecast(self):
        # Starta en tråd för att söka efter Chromecast-enheter utan att blockera GUI
        threading.Thread(target=self._find_chromecast_devices).start()

    def _find_chromecast_devices(self):
        # Söker efter Chromecast-enheter
        chromecasts, _ = get_chromecasts()
        self.chromecasts = chromecasts  # Spara enheterna för senare uppspelning

        # Skicka en signal till huvudtråden med listan över hittade enheter
        self.chromecast_found.emit(self.chromecasts)

    def update_chromecast_combo(self, chromecasts):
        # Uppdatera ComboBox med listan över hittade Chromecast-enheter
        self.comboChromecast.clear()
        if chromecasts:
            for cast in chromecasts:
                self.comboChromecast.addItem(cast.name if hasattr(cast, 'name') else "Okänd enhet")
        else:
            self.comboChromecast.addItem("Inga enheter hittades")

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

    def start_playback(self):
    # Välj Chromecast-enheten från ComboBox
     selected_index = self.comboChromecast.currentIndex()
    
    # Kontrollera om en enhet är vald och en videofil finns
     if selected_index >= 0 and self.video_file:
        cast = self.chromecasts[selected_index]
        cast.wait()  # Vänta tills Chromecast är redo

        # Ange URL till videon
        media_url = f"http://din_server_ip:5000/media/{self.video_file.get_filename()}"

        # Om undertextfil finns, ange undertext-URL och MIME-typ
        subtitle_url = None
        if self.subtitle_file:
            subtitle_url = self.subtitle_file.get_subtitle_url()

        # Starta uppspelningen med eller utan undertext-URL
        cast.media_controller.play_media(
            media_url,
            'video/mp4',
            subtitles=subtitle_url,
            subtitle_mime_type='text/srt' if subtitle_url else None
        )

        # Blockera tills uppspelningen är aktiv
        cast.media_controller.block_until_active()
     else:
        # Visa varningsmeddelande om ingen enhet eller fil är vald
        QMessageBox.warning(self, "Fel", "Välj en Chromecast och en videofil innan du spelar upp.")

