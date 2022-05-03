import time

import keyboard
import pyaudio
import numpy as np
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QSlider, QLabel
from scipy import signal as sg


class AUDIO:
    def __init__(self, volume, freq, duration, samplerate):
        self.volume = volume
        self.volume2 = volume
        self.freq = freq
        self.duration = duration
        self.samplerate = samplerate
        self.p = pyaudio.PyAudio()
        self.samples = (np.sin(2 * np.pi * np.arange(samplerate * duration) * freq / samplerate)).astype(np.float32)
        self.samples2 = (np.sin(2 * np.pi * np.arange(samplerate * duration) * freq / samplerate)).astype(np.float32)
        self.wavetype = 0
        self.wavetype2 = 0
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True)

    def set_volume(self, volume):
        self.volume = volume

    def set_volume2(self, volume):
        self.volume2 = volume

    def set_freq(self, freq):
        self.freq = freq
        self.set_wavetype2(self.wavetype2)
        self.set_wavetype(self.wavetype)

    def set_duration(self, duration):
        self.duration = duration

    def set_wavetype(self, wavetype):
        self.wavetype = wavetype
        if self.wavetype == 0:
            self.samples = (
                np.sin(2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)
        if self.wavetype == 1:
            self.samples = (sg.sawtooth(
                2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)
        if self.wavetype == 2:
            self.samples = (
                sg.square(2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)

    def set_wavetype2(self, wavetype):
        self.wavetype2 = wavetype
        if self.wavetype2 == 0:
            self.samples2 = (
                np.sin(2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)
        if self.wavetype2 == 1:
            self.samples2 = (sg.sawtooth(
                2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)
        if self.wavetype2 == 2:
            self.samples2 = (
                sg.square(2 * np.pi * np.arange(self.samplerate * self.duration) * self.freq / self.samplerate)).astype(
                np.float32)

    def play(self, freq):
        if mainWindow.toggleButton.isChecked():
            self.set_freq(freq)
            print(self.freq)
            self.stream.write((self.volume * self.samples))
            # self.stream.write(((self.volume * self.samples) + (self.volume2 * self.samples2))/(self.volume+self.volume2+0.01))

    def play_by_key(self, freq):
        if not mainWindow.toggleButton.isChecked():
            for button in mainWindow.buttons:
                if float(button.text()) == freq:
                    temp = button.styleSheet()
                    button.setStyleSheet('color: lightgray; background-color: lightgray')
                    self.set_freq(freq)
                    print(self.freq)
                    self.stream.write((self.volume * self.samples))
                    button.setStyleSheet(temp)


            # self.stream.write(((self.volume * self.samples) + (self.volume2 * self.samples2))/(self.volume+self.volume2+0.01))

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


##################################################################################


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        a= 10
        b = 20
        print(a, b == b, a)
        # Oknow główne
        self.setFixedSize(530, 440)
        self.setWindowTitle('EPICKI PROJEKT')
        self.setStyleSheet("background-color: gray;")

        # super buttony
        self.buttons = []
        self.frequencies = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30,
                            440.00,466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61,
                            880.00,
                            987.77, 1046.50, 1108.73, 1174.66]

        size = 25
        for i in range(size):
            self.buttons.append(QPushButton(self))

        i = 0
        j = 0
        l = 0
        w = 0
        listh = [1, 3, 6, 8, 10, 13, 15, 18, 20, 22]
        for button in self.buttons:
            button.setText(str(self.frequencies[j]))
            if j in listh:
                button.setStyleSheet('background-color: black')
                l = 50
                w = 10
                button.setGeometry(50 + i, 50, 10, 50)
                i += 11
            else:
                # button.setStyleSheet('background-color: white')
                button.setStyleSheet('color: white; background-color: white')
                l = 90
                w = 20
                button.setGeometry(50 + i, 50, 20, 90)
                i += 21

            button.clicked.connect(lambda checked, text=self.frequencies[j]: button_clicked(text))

            j += 1

        volumeSlider = QSlider(Qt.Vertical, self)
        volumeSlider.setFocusPolicy(Qt.NoFocus)
        volumeSlider.setRange(0, 100)
        volumeSlider.setPageStep(5)
        volumeSlider.setGeometry(50, 200, 30, 100)
        volumeSlider.valueChanged.connect(change_volume)

        durationSlider = QSlider(Qt.Vertical, self)
        durationSlider.setFocusPolicy(Qt.NoFocus)
        durationSlider.setRange(0, 600)
        durationSlider.setPageStep(10)
        durationSlider.setGeometry(100, 200, 30, 100)
        durationSlider.valueChanged.connect(change_duration)

        wavetypeSlider = QSlider(Qt.Vertical, self)
        wavetypeSlider.setFocusPolicy(Qt.NoFocus)
        wavetypeSlider.setRange(0, 2)
        wavetypeSlider.setPageStep(1)
        wavetypeSlider.setGeometry(150, 200, 30, 100)
        wavetypeSlider.valueChanged.connect(change_wavetype)

        volumeSlider2 = QSlider(Qt.Vertical, self)
        volumeSlider2.setFocusPolicy(Qt.NoFocus)
        volumeSlider2.setRange(0, 100)
        volumeSlider2.setPageStep(5)
        volumeSlider2.setGeometry(50, 350, 30, 100)
        volumeSlider2.valueChanged.connect(change_volume2)

        wavetypeSlider2 = QSlider(Qt.Vertical, self)
        wavetypeSlider2.setFocusPolicy(Qt.NoFocus)
        wavetypeSlider2.setRange(0, 2)
        wavetypeSlider2.setPageStep(1)
        wavetypeSlider2.setGeometry(150, 350, 30, 100)
        wavetypeSlider2.valueChanged.connect(change_wavetype2)

        volumeSlider2.setVisible(0)
        wavetypeSlider2.setVisible(0)
        self.setFixedSize(530, 400)

        self.volumeLabel = QLabel("volume", self)
        self.durationLabel = QLabel("duration", self)
        self.wavetypeLabel = QLabel("wave", self)

        self.volumeLabel.move(50, 300)
        self.durationLabel.move(95, 300)
        self.wavetypeLabel.move(150, 300)

        self.sineLabel = QLabel("sine", self)
        self.sawLabel = QLabel("saw", self)
        self.squareLabel = QLabel("square", self)

        self.sineLabel.move(190, 277)
        self.sawLabel.move(190, 233)
        self.squareLabel.move(190, 187)

        self.toggleButton = QPushButton("Keyboard", self)
        self.toggleButton.setGeometry(300, 230, 120, 40)
        self.toggleButton.setCheckable(True)
        self.toggleButton.clicked.connect(self.changeColor)
        self.toggleButton.setStyleSheet("background-color : lightblue")

        # show all the widgets
        self.update()
        self.show()

        # method called by button

    def changeColor(self):
        print(self.toggleButton.isChecked())
        print(self.toggleButton.text())
        # if button is checked
        if self.toggleButton.isChecked():
            # setting background color to light-blue
            self.toggleButton.setText("Mouse")
        # if it is unchecked
        else:
            # set background color back to light-grey
            self.toggleButton.setText("Keyboard")


def change_volume(value):
    a.set_volume(value / 100)


def change_duration(value):
    a.set_duration(value / 100)


def change_wavetype(value):
    a.set_wavetype(value)


def change_volume2(value):
    a.set_volume2(value / 100)


def change_wavetype2(value):
    a.set_wavetype2(value)


def button_clicked(text):
    a.play(text)
    print(text)


if __name__ == '__main__':
    a = AUDIO(0, 440, 0, 44100)

    # b = AUDIO(1, 440, 2, 44100)

    app = QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()

    keyboard.on_press_key("a", lambda _: a.play_by_key(mainWindow.frequencies[0]))  # C
    keyboard.on_press_key("w", lambda _: a.play_by_key(mainWindow.frequencies[1]))  # C#
    keyboard.on_press_key("s", lambda _: a.play_by_key(mainWindow.frequencies[2]))  # D
    keyboard.on_press_key("e", lambda _: a.play_by_key(mainWindow.frequencies[3]))  # D#
    keyboard.on_press_key("d", lambda _: a.play_by_key(mainWindow.frequencies[4]))  # E
    keyboard.on_press_key("f", lambda _: a.play_by_key(mainWindow.frequencies[5]))  # F
    keyboard.on_press_key("t", lambda _: a.play_by_key(mainWindow.frequencies[6]))  # F#
    keyboard.on_press_key("g", lambda _: a.play_by_key(mainWindow.frequencies[7]))  # G
    keyboard.on_press_key("y", lambda _: a.play_by_key(mainWindow.frequencies[8]))  # G#
    keyboard.on_press_key("h", lambda _: a.play_by_key(mainWindow.frequencies[9]))  # A
    keyboard.on_press_key("u", lambda _: a.play_by_key(mainWindow.frequencies[10]))  # A#
    keyboard.on_press_key("j", lambda _: a.play_by_key(mainWindow.frequencies[11]))  # H
    keyboard.on_press_key("k", lambda _: a.play_by_key(mainWindow.frequencies[12]))  # C
    keyboard.on_press_key("o", lambda _: a.play_by_key(mainWindow.frequencies[13]))  # C#
    keyboard.on_press_key("l", lambda _: a.play_by_key(mainWindow.frequencies[14]))  # D
    keyboard.on_press_key("p", lambda _: a.play_by_key(mainWindow.frequencies[15]))  # D#
    keyboard.on_press_key(";", lambda _: a.play_by_key(mainWindow.frequencies[16]))  # E
    keyboard.on_press_key("'", lambda _: a.play_by_key(mainWindow.frequencies[17]))  # F
    keyboard.on_press_key("]", lambda _: a.play_by_key(mainWindow.frequencies[18]))  # F#
    keyboard.on_press_key("\\", lambda _: a.play_by_key(mainWindow.frequencies[19]))  # G

    sys.exit(app.exec())

###################################################################################


