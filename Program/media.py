import os
import threading
from PyQt5.QtCore import pyqtSignal
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
        self.content_type = "video/h264"

    def play(self, play_media_func):
        play_media_func(self.get_filename())

#class SubtitleFile(MediaFile):
    #def __init__(self, file_path):
        #super().__init__(file_path)
        #self.content_type = "text/srt"

   # def get_subtitle_url(self):
       # return f"http://din_server_ip:5000/subtitles/{self.get_filename()}"

class ChromecasterGUI(QMainWindow, Ui_Chromecaster):
    # Definiera en signal för att uppdatera Chromecast-listan i ComboBox
    chromecast_found = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.video_file = None
        #self.subtitle_file = None
        self.chromecasts = []  # Lagra hittade Chromecast-enheter

        # Koppla knapparna till funktioner
        self.btnVideo.clicked.connect(self.select_video_file)
       # self.btnSRT.clicked.connect(self.select_subtitle_file)
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

    #def select_subtitle_file(self):
       # file_path, _ = QFileDialog.getOpenFileName(self, "Välj undertextsfil", "", "Subtitle Files (*.srt)")
        #if file_path:
         #   self.subtitle_file = SubtitleFile(file_path)
          #  self.txtSRT.setText(self.subtitle_file.get_filename())

    def start_playback(self):
     selected_index = self.comboChromecast.currentIndex()
    
     if selected_index >= 0 and self.video_file:
        cast = self.chromecasts[selected_index]
        cast.wait()

        # Sätt rätt IP-adress och port till media_url
        media_url = f"http://192.168.0.245:5500/Media/{self.video_file.get_filename()}"

        try:
            # Starta uppspelningen
            cast.media_controller.play_media(media_url, 'video/mp4', stream_type='BUFFERED')
            cast.media_controller.block_until_active()
 
            # Logga status för felsökning
            print(cast.media_controller.status)

        except Exception as e:
            print(f"Fel vid uppspelning: {e}")
            QMessageBox.warning(self, "Fel", f"Uppspelningsfel: {e}")

     else:
        QMessageBox.warning(self, "Fel", "Välj en Chromecast och en videofil innan du spelar upp.")


