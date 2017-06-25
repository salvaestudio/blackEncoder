#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import subprocess
import shlex

# Global variables

fileinput = ''
fileaudio = ''
fileoutput = ''

# Code of ffmpeg according to the cases of Checkbox

comandoMkt = '\
ffmpeg \
-f lavfi \
-i color=c=black:s=1920x1080:r=25:d=1 \
-f lavfi \
-i "aevalsrc=0:c=stereo:d=1" \
-i {} -filter_complex \
"[0:v] trim=start_frame=1:end_frame=3 [blackstart]; \
[0:v] trim=start_frame=1:end_frame=5 [blackend]; \
[1:a] atrim=duration=0.12 [audiostart]; \
[1:a] atrim=duration=0.2 [audioend]; \
[blackstart] [audiostart] [2:v] [2:a] [blackend] [audioend] concat=n=3:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v qtrle \
-c:a pcm_s24le \
-ar 48000 \
-timecode 00:02:00:00 {}'

comandoPubli = '\
ffmpeg \
-f lavfi \
-i color=c=black:s=1920x1080:r=25:d=1 \
-f lavfi \
-i "aevalsrc=0:c=stereo:d=1" \
-i {} -filter_complex \
"[0:v] trim=start_frame=1:end_frame=5 [blackstart]; \
[0:v] trim=start_frame=1:end_frame=5 [blackend]; \
[1:a] atrim=duration=0.2 [audiostart]; \
[1:a] atrim=duration=0.2 [audioend]; \
[blackstart] [audiostart] [2:v] [2:a] [blackend] [audioend] concat=n=3:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v qtrle \
-c:a pcm_s24le \
-ar 48000 \
-timecode 01:00:00:00 {}'

comandoAg = '\
ffmpeg \
-f lavfi \
-i color=c=black:s=1920x1080:r=25:d=1 \
-f lavfi -i "aevalsrc=0:c=stereo:d=1" \
-i {} -filter_complex \
"[0:v] trim=start_frame=1:end_frame=5 [blackstart]; \
[0:v] trim=start_frame=1:end_frame=5 [blackend]; \
[1:a] atrim=duration=0.2 [audiostart]; [1:a] atrim=duration=0.2 [audioend]; \
[blackstart] [audiostart] [2:v] [2:a] [blackend] [audioend] concat=n=3:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v libx264 \
-crf 18 \
-preset slow \
-profile:v high10 \
-pix_fmt yuv420p \
-c:a aac -strict -2 \
-b:a 128k \
-timecode 00:01:00:00 \
-tune zerolatency {}'

comandoMailhi = '\
ffmpeg \
-f lavfi \-i color=c=black:s=1280x720:r=25:d=1 \
-f lavfi -i "aevalsrc=0:c=stereo:d=1" \
-i {} -filter_complex \
"[0:v] trim=start_frame=1:end_frame=5 [blackstart]; \
[0:v] trim=start_frame=1:end_frame=5 [blackend]; \
[2:v] scale=1280:-1 [scaled]; \
[1:a] atrim=duration=0.2 [audiostart]; \
[1:a] atrim=duration=0.2 [audioend]; \
[blackstart] [audiostart] [scaled] [2:a] [blackend] [audioend] concat=n=3:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v libx264 \
-crf 22 \
-preset slow \
-profile:v high10 \
-pix_fmt yuv420p \
-c:a aac -strict -2 \
-b:a 128k \
-timecode 00:01:00:00 \
-tune zerolatency {}'

comandoMaillow = '\
ffmpeg \
-f lavfi \
-i color=c=black:s=1280x720:r=25:d=1 \
-f lavfi -i "aevalsrc=0:c=stereo:d=1" \
-i {} -filter_complex \
"[0:v] trim=start_frame=1:end_frame=5 [blackstart]; \
[0:v] trim=start_frame=1:end_frame=5 [blackend]; \
[2:v] scale=1280:-1 [scaled]; \
[1:a] atrim=duration=0.2 [audiostart]; \
[1:a] atrim=duration=0.2 [audioend]; \
[blackstart] [audiostart] [scaled] [2:a] [blackend] [audioend] concat=n=3:v=1:a=1[v][a]" \
-map "[v]" \
-map "[a]" \
-c:v libx264 \
-crf 32 \
-preset slow \
-profile:v high10 \
-pix_fmt yuv420p \
-c:a aac -strict -2 \
-b:a 128k \
-timecode 00:01:00:00 \
-tune zerolatency {}'

comandoAudio = '\
ffmpeg \
-i {} -i {} \
-c:v copy \
-c:a copy \
-map 0:v \
-map 1:a {}'


class Window(QtGui.QMainWindow):
    def __init__(self) -> object:
        super(Window, self).__init__()
        self.setGeometry(50, 50, 460, 400)
        self.setWindowTitle("Super ENCODER")
        self.setWindowIcon(QtGui.QIcon('/home/salva/Imágenes/skull-01.png'))

        extractAction = QtGui.QAction("&EXIT", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):

        btn4 = QtGui.QPushButton("Select input file", self)
        btn4.clicked.connect(self.inputfile)
        btn4.resize(120, 30)
        btn4.move(60, 160)

        btn5 = QtGui.QPushButton("Select audio file", self)
        btn5.clicked.connect(self.audiofile)
        btn5.resize(120, 30)
        btn5.move(60, 190)

        btn6 = QtGui.QPushButton("Save file", self)
        btn6.clicked.connect(self.outputfile)
        btn6.resize(120, 30)
        btn6.move(60, 220)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(60, 270, 280, 20)

        self.btn = QtGui.QPushButton("Encode!", self)
        self.btn.move(60, 300)
        self.btn.resize(120, 30)
        self.btn.clicked.connect(self.actionEnc)

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItem(" Pauta marketing")
        self.comboBox.addItem(" Pauta publicidad")
        self.comboBox.addItem(" Para agencia")
        self.comboBox.addItem(" Para mail alta")
        self.comboBox.addItem(" Para mail baja")
        self.comboBox.addItem(" Unir audio a imagen")
        self.comboBox.move(60, 60)
        self.comboBox.resize(160, 50)

        self.labelintro = QtGui.QLabel("Select option to encode:", self)
        self.labelintro.move(60, 36)
        self.labelintro.resize(180, 20)
        self.labelintro.hasScaledContents()

        self.labelinput = QtGui.QLabel("File input", self)
        self.labelinput.move(200, 160)
        self.labelinput.resize(140, 30)
        self.labelinput.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.labelaudio = QtGui.QLabel("Only if it is necessary", self)
        self.labelaudio.move(200, 190)
        self.labelaudio.resize(140, 30)
        self.labelaudio.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.labeloutput = QtGui.QLabel("File out", self)
        self.labeloutput.move(200, 220)
        self.labeloutput.resize(140, 30)
        self.labeloutput.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.comboBox.activated[str].connect(self.getItem)

        self.show()

    def getItem(self):
        global item
        item = self.comboBox.currentIndex()

    def inputfile(self):
        global fileinput
        fileinput = QtGui.QFileDialog.getOpenFileName(None, "Select file to encode", "/home/salva",
                                                      "video files (*.avi *.mkv *.mp4 *.mov *.mpg);; All files (*)")
        self.labelinput.setText(fileinput)

    def audiofile(self):
        global fileaudio
        fileaudio = QtGui.QFileDialog.getOpenFileName(None, "Select audio file", "/home/salva",
                                                      "audio files (*.aiff *.wav *.mp3);; All files (*)")
        self.labelaudio.setText(fileaudio)

    def outputfile(self):
        global fileoutput
        fileoutput = QtGui.QFileDialog.getSaveFileName(None, "Select output file", "/home/salva",
                                                       "video files (*.avi *.mkv *.mp4 *.mov *.mpg);; All files (*)")
        self.labeloutput.setText(fileoutput)

    def execffmpeg(self):
        if item == 0:
            self.encodeMkt()
        elif item == 1:
            self.encodePubli()
        elif item == 2:
            self.encodeAg()
        elif item == 3:
            self.encodeMailhi()
        elif item == 4:
            self.encodeMaillow()
        elif item == 5:
            self.encodeAudio()
        else:
            WinError().exec_()

    def actionEnc(self):
        self.encoding()
        if len(fileinput) == 0:
            Tercera().exec_()
        elif len(fileoutput) == 0:
            Tercera().exec_()
        elif len(fileaudio) == 0:
            if item == 5:
                Tercera().exec_()
            else:
                self.execffmpeg()
        else:
            print('codificando!')
            self.execffmpeg()

    # Progress bar

    def encoding(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)

    # Functions for ffmpeg as chosen in checkbox

    def encodeMkt(self):
        global comandoMkt
        subprocess.call(shlex.split(comandoMkt.format(fileinput, fileoutput + '.mov')))
        Secundaria().exec_()

    def encodePubli(self):
        global comandoPubli
        subprocess.call(shlex.split(comandoPubli.format(fileinput, fileoutput + '.mov')))
        Secundaria().exec_()

    def encodeAg(self):
        global comandoAg
        subprocess.call(shlex.split(comandoAg.format(fileinput, fileoutput + '.mp4')))
        Secundaria().exec_()

    def encodeMailhi(self):
        global comandoMailhi
        subprocess.call(shlex.split(comandoMailhi.format(fileinput, fileoutput + '.mp4')))
        Secundaria().exec_()

    def encodeMaillow(self):
        global comandoMaillow
        subprocess.call(shlex.split(comandoMaillow.format(fileinput, fileoutput + '.mp4')))
        Secundaria().exec_()

    def encodeAudio(self):
        global comandoAudio
        subprocess.call(shlex.split(comandoAudio.format(fileinput, fileaudio, fileoutput + '.mov')))
        Secundaria().exec_()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Exit!',
                                            "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass


def b11_clicked():
    exit()

class Secundaria(QtGui.QDialog):
    def __init__(self):
        super(Secundaria, self).__init__()

        b10 = QtGui.QPushButton("Do another job?", self)
        b10.move(50, 20)
        b10.clicked.connect(self.close)

        b11 = QtGui.QPushButton("Exit", self)
        b11.move(50, 50)
        b11.clicked.connect(b11_clicked)

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle("Work completed. Oh Yeah!")
        self.show()

class Tercera(QtGui.QDialog):
    def __init__(self):
        super(Tercera, self).__init__()

        self.labelmesseng = QtGui.QLabel('Did you indicate input video, \n audio if needed and output file?', self)
        self.labelmesseng.move(40, 0)
        self.labelmesseng.resize(240, 100)
        self.labelmesseng.hasScaledContents()

        b16 = QtGui.QPushButton("Try again", self)
        b16.move(96, 100)
        b16.clicked.connect(self.close)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Missing data!")
        self.show()

class WinError(QtGui.QDialog):
    def __init__(self):
        super(WinError, self).__init__()

        b12 = QtGui.QPushButton("Do another job?", self)
        b12.move(50, 20)
        b12.clicked.connect(self.close)

        b13 = QtGui.QPushButton("Exit", self)
        b13.move(50, 50)
        b13.clicked.connect(b11_clicked)

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle("Something is wrong. Quit or try again")
        self.show()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
