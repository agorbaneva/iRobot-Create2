from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import torch

from utils.ImageWindow import ImageWindow
from utils.WorkerThreads import Worker1
from utils.TimerLCDNumber import TimerLCDNumber
from utils.Slider import Slider
from utils.HighlightEffect import HighlightEffect
from utils.MouseDrawer import MouseDrawer

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # originally 1118, 919
        WIDTH = 1000
        HEIGHT = 980
        VIDEO_WIDTH = 380
        MARGIN = 75
        BUTTONS_GRID_HEIGHT = 279

        # all qRects are in the form of left, top, width, height; top left is 0, 0 on canvas

        MainWindow.resize(WIDTH, HEIGHT)
        MainWindow.setStyleSheet("background-color: rgb(236, 239, 248);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.returnToBase = QtWidgets.QPushButton(self.centralwidget)
        self.returnToBase.setGeometry(QtCore.QRect((WIDTH - MARGIN - VIDEO_WIDTH) + (VIDEO_WIDTH - 191) // 2,
                                                   170 + BUTTONS_GRID_HEIGHT // 2 - 121 // 2, 191, 121))
        self.returnToBase.setObjectName("returnToBase")

        toolbar = QToolBar("My main toolbar")
        MainWindow.addToolBar(toolbar)

        connect = QAction("Connect", MainWindow)
        connect.triggered.connect(self.onConnect)
        toolbar.addAction(connect)

        passive = QAction("Passive", MainWindow)
        passive.triggered.connect(self.onPassive)
        toolbar.addAction(passive)

        safe = QAction("Safe", MainWindow)
        safe.triggered.connect(self.onSafe)
        toolbar.addAction(safe)

        BACKGROUND_COLOR_WHEN_PRESSED = "rgb(226, 221,242)"

        # background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey); border-style: solid;
        self.returnToBase.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                        "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")

        self.returnToBase.setGraphicsEffect(HighlightEffect())

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(MARGIN, 170, 380, BUTTONS_GRID_HEIGHT))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.pathWidget = MouseDrawer()
        self.pathWidget.setGeometry(QtCore.QRect(MARGIN, 170, 380, BUTTONS_GRID_HEIGHT))
        self.gridLayout.addWidget(self.pathWidget)
        self.pathWidget.setGraphicsEffect(HighlightEffect())


        BUTTON_WIDTH = 175
        BUTTON_LENGTH = 40

        # buttons below the Mouse Drawer path widget
        self.clearPathButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearPathButton.setGraphicsEffect(HighlightEffect())
        self.clearPathButton.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                         "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.clearPathButton.setGeometry(MARGIN + self.pathWidget.frameGeometry().width()//4 - BUTTON_WIDTH//2, self.pathWidget.geometry().bottom() + 20, BUTTON_WIDTH, BUTTON_LENGTH)
        self.clearPathButton.clicked.connect(self.pathWidget.clearLines)

        self.followPathButton = QtWidgets.QPushButton(self.centralwidget)
        self.followPathButton.setGraphicsEffect(HighlightEffect())
        self.followPathButton.setStyleSheet("QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
                                         "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.followPathButton.setGeometry(MARGIN + self.pathWidget.frameGeometry().width()*3//4 - BUTTON_WIDTH//2, self.pathWidget.geometry().bottom() + 20, BUTTON_WIDTH, BUTTON_LENGTH)
        # self.followPathButton.clicked.connect(self.pathWidget.followPath())

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setObjectName("title")

        self.title.setGeometry(QtCore.QRect((WIDTH - 400) // 2, 25, 400, 50))
        self.title.setStyleSheet("font: 20pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)")

        self.batterySplitter = QtWidgets.QSplitter(self.centralwidget)
        self.batterySplitter.setObjectName("batterySplitter")
        self.batterySplitter.setGeometry(
            QtCore.QRect((WIDTH - MARGIN - VIDEO_WIDTH) + (VIDEO_WIDTH - 250) // 2, 100, 250, 51))
        self.batterySplitter.setOrientation(QtCore.Qt.Horizontal)

        self.batteryLevel = QtWidgets.QLabel(self.batterySplitter)
        self.batteryLevel.setObjectName("batteryLevel")
        self.batteryLevel.setStyleSheet("font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)")

        self.batteryPercent = TimerLCDNumber(self.batterySplitter)
        self.batteryPercent.setObjectName("batteryPercent")
        self.batteryPercent.setStyleSheet("font: 20 pt \"Century Gothic Bold\";")
        # self.batteryPercent.setValue(self.getBattery())


        # changed from widget to qlabel
        self.video = QtWidgets.QLabel(self.centralwidget)
        self.video.setGeometry(QtCore.QRect(MARGIN, 550, VIDEO_WIDTH, 275))
        self.video.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.video.setObjectName("video")
        self.video.setGraphicsEffect(HighlightEffect())

        CAPTURE_IMAGE_WIDTH = 175
        self.captureImageNewWindow = QtWidgets.QPushButton(self.centralwidget)
        self.captureImageNewWindow.setGeometry(
            QtCore.QRect(MARGIN + VIDEO_WIDTH // 2 - CAPTURE_IMAGE_WIDTH // 2, self.video.geometry().bottom() + 20,
                         CAPTURE_IMAGE_WIDTH, 40))#self.leftTurnButton.height()))
        self.captureImageNewWindow.setStyleSheet(
            "QPushButton {font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)}"
            "QPushButton:pressed { background-color:" + BACKGROUND_COLOR_WHEN_PRESSED + "; }")
        self.captureImageNewWindow.setObjectName("captureImageNewWindow")
        self.captureImageNewWindow.setGraphicsEffect(HighlightEffect())

        # Sub Window
        self.imageWindow = ImageWindow()

        # Button Event
        self.captureImageNewWindow.clicked.connect(self.processImage)

        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setBackground('w')
        self.graphWidget.setXRange(-150, 150)
        self.graphWidget.setYRange(-150, 150)
        self.graphWidget.setTitle("Robot Movement Map")
        self.graphWidget.setLabel('left', 'Vertical Movement')
        self.graphWidget.setLabel('bottom', 'Horizontal Movement')

        points = {'x':[0, 100, 150], 'y':[0, -50, -100]}
        graph  = pg.PlotDataItem(points)

        self.graphWidget.addItem(graph)
        #self.graphWidget.addScatter(0, 0, 0)
        #self.graphWidget.setDefaultPadding(padding=0)

        self.graphWidget.setGeometry(QtCore.QRect(WIDTH - MARGIN - 380, 550, VIDEO_WIDTH, 275))
        self.graphWidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setGraphicsEffect(HighlightEffect())

        self.speedSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.speedSplitter.setGeometry(QtCore.QRect(MARGIN, 100, 321, 51))
        self.speedSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.speedSplitter.setObjectName("speedSplitter")

        self.speedLabel = QtWidgets.QLabel(self.speedSplitter)
        self.speedLabel.setStyleSheet("font: 14pt \"Century Gothic Bold\"; color: rgb(98, 111, 132)")
        self.speedLabel.setObjectName("speedLabel")

        self.speedSlider = Slider(self.speedSplitter)
        self.speedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider.setObjectName("speedSlider")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # create a worker object and start it
        self.model = torch.hub.load('YOLOv5/yolov5', 'custom', path='YOLOv5/pigeon model weights FINAL.pt', source='local', force_reload=True)  # local model
        self.model.conf = 0.9
        self.Worker1 = Worker1(self.model)
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        # create the YOLOv5 model that we will use
        #self.model = torch.hub.load('YOLOv5/yolov5', 'custom', path='YOLOv5/pigeon model weights FINAL.pt', source='local', force_reload=True)  # local model

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1118, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def ImageUpdateSlot(self, Image, foundPigeon):
        # image is value emitted

        if foundPigeon == True:
            print("found!")
        else:
            print("nope!")

        self.video.setPixmap(QPixmap.fromImage(Image))

        self.image = Image

    def processImage(self):
        # self.imageWindow = imageWindow()
        self.imageWindow.setImage(self.image)
        self.imageWindow.show()

    '''
    def CancelFeed(self):
        self.Worker1.stop()
    # create cancel button , do .clicked.connect(self.CancelFeed) etc

    '''

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Recharging Robot GUI"))
        self.returnToBase.setText(_translate("MainWindow", "Return to base"))
        self.clearPathButton.setText(_translate("MainWindow", "Clear Path"))
        self.followPathButton.setText(_translate("MainWindow", "Follow Path"))
        self.title.setText(_translate("MainWindow", "Recharging Robot Interface"))
        self.batteryLevel.setText(_translate("MainWindow", "Battery level:"))
        self.speedLabel.setText(_translate("MainWindow", "Speed:"))
        self.captureImageNewWindow.setText(_translate("MainWindow", "Capture Image"))