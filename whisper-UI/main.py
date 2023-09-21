# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMainWindow, QLabel, QVBoxLayout, QTextEdit, QListWidget, QListWidgetItem
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore

import moviepy.editor as mp
import whisper
import os

class AudioPlayer(QMainWindow):
    def __init__(self, audio_path, audio_text):
        super().__init__()

        self.initUI(audio_path, audio_text)

        self.audio_path = audio_path
        self.audio_text = audio_text

    def initUI(self, audio, text):

        # Create a media player object
        self.player = QMediaPlayer()

        # Create a button to play the audio
        play_button = QPushButton('Play', self)
        play_button.clicked.connect(self.playAudio)
        play_button.setGeometry(15, 15, 100, 30)

        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stopAudio)
        stop_button.setGeometry(130, 15, 100, 30)

        wubingshenyin = QLabel(self)
        wubingshenyin.setText('Flustered Love, Hidden Joy')
        wubingshenyin.setGeometry(260, 15, 200, 30)

        texts = ""

        with open(text, "r", encoding='gbk') as f:  #打开文本
            texts = f.read()   #读取文本
            
        sentances = texts.split(';')

        self.listWidget = QListWidget(self)
        self.listWidget.setWordWrap(True)

        for sentance in sentances:
            listItem = QListWidgetItem(sentance)
            self.listWidget.addItem(listItem)

        self.listWidget.itemClicked.connect(self.on_item_clicked)
        
        self.listWidget.setGeometry(15, 60, 970, 543)

        # Set up the main window
        self.setGeometry(100, 100, 1000, 618)
        self.setWindowTitle('Audio Player')
        self.show()

    def on_item_clicked(self, item):
        # Get the text of the clicked item
        text = item.text()
        time = int(float(str(text).split('|')[0].split(':')[0])*2000)
        print(time)
        file_path = self.audio_path
        media = QMediaContent(QtCore.QUrl.fromLocalFile(file_path))

        # Set the media content to the player
        self.player.setMedia(media)

        self.player.setPosition(time)

        # Play the audio
        self.player.play()

    def playAudio(self):

        print('click the play')

        # Load the audio file
        file_path = self.audio_path
        print(file_path)
        media = QMediaContent(QtCore.QUrl.fromLocalFile(file_path))

        # Set the media content to the player
        self.player.setMedia(media)
        # Play the audio
        self.player.play()

    def stopAudio(self):

        print('click the stop')

        self.player.stop()

class FileSelectorWindow(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('whisper-UI')

        self.button = QPushButton('Select File', self)
        self.button.setGeometry(100, 30, 100, 30)
        self.button.clicked.connect(self.showFileDialog)

    def showFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        # get file path
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)")

        if file_path:
            print(f"Selected file: {file_path}")

            # get file name
            file_path_slice = file_path.split("/")
            file_name = file_path_slice[-1]
            file_name_profix = file_name.split('.')[0]
            
            # get file folder
            file_path_folder = file_path.split(file_name)[0]
            file_path_mp3 = ''

            if file_name.split('.')[1] != 'mp3':
                my_clip = mp.AudioFileClip(file_path)
                file_path_mp3 = file_path_folder + file_name_profix + '.mp3'
                print('converting to mp3, other formats may have error. patience')
                my_clip.write_audiofile(file_path_mp3)
            else:
                file_path_mp3 = file_path

            # determine whether txt file exist
            if os.path.exists(file_path_folder + file_name_profix + ".txt"):

                print('open the audio & text window')
                # open the txt file and load the audio
                self.audio_window = AudioPlayer(file_path_mp3, file_path_folder + file_name_profix + ".txt")
                self.audio_window.show()

                # open a now window and close this window

            else:

                print("converting has began, please wait (ᗜ ˰ ᗜ) ")
                print("it will take a pretty long time (ᗜ ˰ ᗜ)")
                # convert the file first
                model = whisper.load_model("small")
                result = model.transcribe(file_path)
                
                print('already get result, begin to write to txt file.')

                for item in result['segments']:
                    line = str(item['start']) + ':' + str(item['end']) + '|' + item['text'] + ';'
                    with open(file_path_folder + file_name_profix + ".txt","a") as f:
                        f.write(line)
                
                print('writing is over')
                self.audio_window = AudioPlayer(file_path_mp3, file_path_folder + file_name_profix + ".txt")
                self.audio_window.show()

                # open a now window and close this window
            

        else:
            print("No file selected")

if __name__ == '__main__':

    print("whisper-GUI create by Chenyang based on QyPt5. (ᗜ ˰ ᗜ)")

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    file_select_window = FileSelectorWindow()
    file_select_window.show()

    

    sys.exit(app.exec_())
