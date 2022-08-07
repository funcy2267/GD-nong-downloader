# This Python file uses the following encoding: utf-8
import sys

import requests
import subprocess
from io import BytesIO
from zipfile import ZipFile

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_downloadSong.clicked.connect(downloadSong)
        self.ui.actionDownload_ytdl.triggered.connect(downloadYtdl)
        self.ui.actionDownload_ffmpeg.triggered.connect(downloadFfmpeg)

gd_music = "%localappdata%/GeometryDash/"

def downloadFile(url, destination):
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)

def downloadYtdl():
    downloadFile("https://yt-dl.org/downloads/2021.12.17/youtube-dl.exe", "youtube-dl.exe")

def downloadFfmpeg():
    r = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
    with ZipFile(BytesIO(r.content)) as zf, open("ffmpeg.exe", "wb") as f:
        f.write(zf.read(zf.namelist()[0]+'bin/ffmpeg.exe'))

def downloadSong():
    song_link = widget.ui.lineEdit_link.text()
    song_id = widget.ui.lineEdit_id.text()
    song_bitrate = widget.ui.comboBox_bitrate.currentText()
    subprocess.call(["youtube-dl.exe", song_link, "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", "--audio-quality", song_bitrate, "-o", gd_music+song_id+".mp3", "--force-ipv4"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
