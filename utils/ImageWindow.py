from PyQt5 import QtCore, QtWidgets
from utils.HighlightEffect import HighlightEffect
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        WINDOW_WIDTH = 900
        WINDOW_HEIGHT = WINDOW_WIDTH * 3 // 5
        PICTURE_WIDTH = 400
        PICTURE_HEIGHT = 300
        BACKGROUND_COLOR_WHEN_PRESSED = "rgb(226, 221,242)"
        MARGIN = 20

        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-color: rgb(236, 239, 248);")

        self.label = QLabel(self)
        self.label.setGraphicsEffect(HighlightEffect())

        self.label.setGeometry(
            QtCore.QRect(WINDOW_WIDTH // 2 - PICTURE_WIDTH // 2, WINDOW_HEIGHT // 2 - PICTURE_HEIGHT // 2,
                         PICTURE_WIDTH, PICTURE_HEIGHT))

        self.leftLayoutWidget = QtWidgets.QWidget(self)

        self.title = QtWidgets.QLabel(self)
        self.title.setObjectName("title")
        self.title.setGeometry(QtCore.QRect((WINDOW_WIDTH - 240) // 2, 25, 240, 50))
        self.title.setStyleSheet("font: 20pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)")

        LAYOUT_WIDTH = 200
        LAYOUT_HEIGHT = WINDOW_HEIGHT // 2
        self.leftLayoutWidget.setGeometry(
            QtCore.QRect(MARGIN, WINDOW_HEIGHT // 2 - LAYOUT_HEIGHT // 2, LAYOUT_WIDTH, WINDOW_HEIGHT // 2))

        self.gridLayout = QtWidgets.QGridLayout(self.leftLayoutWidget)
        self.gridLayout.setContentsMargins(3, 0, 0, 0)

        self.button1 = QtWidgets.QPushButton(self.leftLayoutWidget)
        self.button1.setObjectName("button1")

        self.button1.setGraphicsEffect(HighlightEffect())
        self.button1.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.gridLayout.addWidget(self.button1, 1, 0, 1, 1)
        self.button2 = QtWidgets.QPushButton(self.leftLayoutWidget)
        self.button2.setObjectName("button2")
        self.button2.setGraphicsEffect(HighlightEffect())
        self.button2.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.gridLayout.addWidget(self.button2, 2, 0, 1, 1)

        self.button3 = QtWidgets.QPushButton(self.leftLayoutWidget)
        self.button3.setObjectName("button3")
        self.gridLayout.addWidget(self.button3, 3, 0, 1, 1)
        self.button3.setGraphicsEffect(HighlightEffect())
        self.button3.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")

        self.rightLayoutWidget = QtWidgets.QWidget(self)

        self.rightLayoutWidget.setGeometry(
            QtCore.QRect(WINDOW_WIDTH - MARGIN - LAYOUT_WIDTH, WINDOW_HEIGHT // 2 - LAYOUT_HEIGHT // 2, LAYOUT_WIDTH,
                         WINDOW_HEIGHT // 2))

        self.gridLayout = QtWidgets.QGridLayout(self.rightLayoutWidget)
        self.gridLayout.setContentsMargins(3, 0, 0, 0)

        self.button4 = QtWidgets.QPushButton(self.rightLayoutWidget)
        self.button4.setObjectName("button4")

        self.button4.setGraphicsEffect(HighlightEffect())
        self.button4.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.gridLayout.addWidget(self.button4, 1, 0, 1, 1)
        self.button5 = QtWidgets.QPushButton(self.rightLayoutWidget)
        self.button5.setObjectName("button5")
        self.button5.setGraphicsEffect(HighlightEffect())
        self.button5.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.gridLayout.addWidget(self.button5, 2, 0, 1, 1)

        self.button6 = QtWidgets.QPushButton(self.rightLayoutWidget)
        self.button6.setObjectName("button6")
        self.button6.setGraphicsEffect(HighlightEffect())
        self.button6.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                   "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.gridLayout.addWidget(self.button6, 3, 0, 1, 1)

        self.retranslate_UI()

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setAlignment(Qt.AlignCenter)

    def image(self):
        pixmap = self.label.QPixmap.pixmap()
        image = pixmap.toImage()
        return image

        # return the image here

    def retranslate_UI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("imageWindow", "Analyzing Snapshot Image"))
        self.title.setText(_translate("imageWindow", "Snapshot Image"))