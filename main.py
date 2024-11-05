import sys
from PyQt5.QtWidgets import QApplication
from media import ChromecasterGUI
from backend import play_media

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChromecasterGUI()
    window.show()
    sys.exit(app.exec_())