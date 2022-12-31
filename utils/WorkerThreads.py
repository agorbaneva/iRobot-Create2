from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PIL
import cv2
import io
import socket
import struct
import numpy
from PIL import Image


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage, bool)

    def __init__(self, model=None, parent=None):
        QThread.__init__(self, parent)
        # loading custom model
        self.model = model
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.server_socket = socket.socket()
        # uncomment below to connect Pi Camera Module V2
        # self.server_socket.bind(('x.x.x.x', 8000))  # ADD IP HERE
        # self.server_socket.listen(0)
        # self.count = 0

    def run(self):
        # change this to True if you want to connect the Pi Camera Module V2 to the GUI and uncomment below
        self.ThreadActive = False # True

        # conn, addr = self.server_socket.accept()
        # connection = conn.makefile('rb')



        while self.ThreadActive:
            # get a single frame from our window
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if image_len:

                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                frame = PIL.Image.open(image_stream)
                Image = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)

                #Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # flip image on vertical axes
                #FlippedImage = cv2.flip(Image, 1)
                self.count += 1
                results = self.model(Image)

                if len(results.xyxy[0]) > 0:
                    foundPigeons = True
                else:
                    foundPigeons = False

                results.save(save_dir="YOLOv5")

                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(411, 300, Qt.KeepAspectRatio)

                # when emit function is called, will send a message to main window class
                self.ImageUpdate.emit(Pic, foundPigeons)
        #Capture = cv2.VideoCapture(0)  # using video web cam here, don't use if using Camera Module
