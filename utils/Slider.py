from PyQt5 import QtCore, QtWidgets

class Slider(QtWidgets.QSlider):
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Right, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
            return
        super(Slider, self).keyPressEvent(event)