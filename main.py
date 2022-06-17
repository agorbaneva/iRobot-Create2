# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
import sys
import serial
import struct

from PyQt5 import QtWidgets
from utils.design import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox




connection = None
VELOCITYCHANGE = 200
ROTATIONCHANGE = 200


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    callbackKeyUp = False
    callbackKeyDown = False
    callbackKeyLeft = False
    callbackKeyRight = False
    callbackKeyLastDriveCommand = ''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        k = e.key()
        print(e.key())
        motionChange = False

        if k == Qt.Key_W:
            print("up?")
            self.callbackKeyUp = True
            motionChange = True
        elif k == Qt.Key_S:
            self.callbackKeyDown = True
            motionChange = True
        elif k == Qt.Key_A:
            self.callbackKeyLeft = True
            motionChange = True
        elif k == Qt.Key_D:
            self.callbackKeyRight = True
            motionChange = True
        elif k == Qt.Key_P:
            self.sendCommandASCII('140 3 8 60 16 62 16 64 16 65 16 67 16 69 16 71 16 72 16 141 3')
        else:
            super().keyPressEvent(e)

        if motionChange == True:
            velocity = 0
            velocity += VELOCITYCHANGE if self.callbackKeyUp is True else 0
            velocity -= VELOCITYCHANGE if self.callbackKeyDown is True else 0
            rotation = 0
            rotation += ROTATIONCHANGE if self.callbackKeyLeft is True else 0
            rotation -= ROTATIONCHANGE if self.callbackKeyRight is True else 0

            # compute left and right wheel velocities
            vr = int(velocity + (rotation / 2))
            vl = int(velocity - (rotation / 2))

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    def keyReleaseEvent(self, e):
        k = e.key()
        motionChange = False

        if k == Qt.Key_W:
            self.callbackKeyUp = False
            motionChange = True
        elif k == Qt.Key_S:
            self.callbackKeyDown = False
            motionChange = True
        elif k == Qt.Key_A:
            self.callbackKeyLeft = False
            motionChange = True
        elif k == Qt.Key_D:
            self.callbackKeyRight = False
            motionChange = True
        else:
            super().keyReleaseEvent(e)

        if motionChange == True:
            velocity = 0
            velocity += VELOCITYCHANGE if self.callbackKeyUp is True else 0
            velocity -= VELOCITYCHANGE if self.callbackKeyDown is True else 0
            rotation = 0
            rotation += ROTATIONCHANGE if self.callbackKeyLeft is True else 0
            rotation -= ROTATIONCHANGE if self.callbackKeyRight is True else 0

            # compute left and right wheel velocities
            vr = int(velocity + (rotation / 2))
            vl = int(velocity - (rotation / 2))

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd


    def setBattery(self):
        global connection
        print("looking for battery")

        if connection is not None:
            self.sendCommandASCII('142 22')
            data = self.get16Unsigned()
            print("data)", data)
            if type(data) is not int:
                return 0

            percent_battery = int(data / 65535 * 100)

            # self.batteryPercent.display(percent_battery)
            return percent_battery

        return 0

    def moveOnPath(self):
        global connection
        movements = self.pathWidget.followPath()
        print("movements", movements)
        if connection is not None and len(movements) > 0:
            # MAKE ROBOT MOVE BASED ON MOVEMENT VARIABLE

            # Special cases:
            # Straight = 32768 or 32767 = 0x8000 or 0x7FFF
            # Turn in place
            # clockwise = -1 = 0xFFFF
            # Turn in place
            # counter-clockwise = 1 = 0x0001

            for line, [distance, turn, direction] in movements.items():
                print("on line ", line)
                # one pixel is currently equal to one centimeter, with this conversion
                distance = distance * 10

                velocity = 200

                if direction == 'L':
                    rotation = 1
                else:
                    rotation = -1


                print(line, distance, turn, direction, rotation)

                # create drive command
                if connection is not None:
                    #make sure its on safe mode
                    self.onSafe()


                    cmd = struct.pack(">Bhh", 137, velocity, rotation)
                    self.sendCommandRaw(cmd)

                    # clearing data
                    self.sendCommandASCII('142 20')
                    self.get16Signed()

                    angle = -2

                    print("before turning, current values: ", velocity, rotation, angle, turn)

                    count = 0
                    while angle * rotation < turn and connection is not None:
                        if count == 10:
                            cmd = struct.pack(">Bhh", 137, 0, 0)
                            self.sendCommandRaw(cmd)
                            break
                        self.sendCommandASCII('142 20')
                        data = self.get16Signed()
                        print("printing signed data inside", data)
                        if -100 < data < 100:
                            angle += data
                        print("angle", angle)
                        # if the robot hasnt moved, indicating some block or program error
                        if data == 0:
                            count += 1
                        else:
                            count = 0
                        if cmd != self.callbackKeyLastDriveCommand:
                            self.sendCommandRaw(cmd)
                            self.callbackKeyLastDriveCommand = cmd
                    cmd = struct.pack(">Bhh", 137, 0, 0)
                    self.sendCommandRaw(cmd)

                if connection is not None:
                    # go straight
                    cmd = struct.pack(">Bhh", 137, velocity, 0)
                    self.sendCommandRaw(cmd)

                    # clearing data
                    self.sendCommandASCII('142 19')
                    self.get16Signed()

                    travelled = 0
                    count = 0
                    while travelled < distance and connection is not None:
                        if count == 10:
                            cmd = struct.pack(">Bhh", 137, 0, 0)
                            self.sendCommandRaw(cmd)

                            break
                        self.sendCommandASCII('142 19')
                        data = self.get16Signed()
                        if -100 < data < 100:
                            travelled += data
                        print(travelled, " travelled")

                        # if the robot hasnt moved, indicating some block or program error

                        if data == 0:
                            count += 1
                        else:
                            count = 0

                    cmd = struct.pack(">Bhh", 137, 0, 0)

                    #cmd = struct.pack(">Bhh", 137, 0, 0)
                    self.sendCommandRaw(cmd)


            print(self.pathWidget.followPath(), connection)
            print("finished!")
            return

    def base(self):
        global connection
        print("clicked")
        if connection is not None:
            self.sendCommandASCII('143')

    def sendCommandASCII(self, command):
        cmd = bytes([int(v) for v in command.split()])
        self.sendCommandRaw(cmd)

    def onConnect(self):
        global connection
        if connection is not None:
            # already connected? do nothing
            return
        try:
            # c = fabric.Connection("192.168.3.151", port=22, user="dragonfly", connect_kwargs={'password': 'dragonfly'})
            connection = serial.Serial('COM3', baudrate=115200, timeout=1)
            print("Connected!")
            print(connection)
            # self.forwardButton.clicked.connect(self.getBattery)
            self.returnToBase.clicked.connect(self.base)
            self.followPathButton.clicked.connect(self.moveOnPath)

            self.batteryPercent.setValue(self.setBattery())
            # self._timerId = self.startTimer(1000)

        except:
            connection = None
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Robot failed to connect. Check your connection!")
            x = msg.exec_()

            print("Connection failed")

    def onSafe(self):
        global connection
        self.sendCommandASCII("131")

    def onPassive(self):
        global connection
        self.sendCommandASCII("128")

    def sendCommandRaw(self, command):
        global connection

        try:
            if connection is not None:
                assert isinstance(command, bytes), 'Command must be of type bytes'
                connection.write(command)
                connection.flush()
            else:
                # tkinter.messagebox.showerror('Not connected!', 'Not connected to a robot!')
                print("Not connected.")
        except serial.SerialException:
            print("Lost connection")
            # tkinter.messagebox.showinfo('Uh-oh', "Lost connection to the robot!")
            connection = None

    def get16Unsigned(self):
        return self.getDecodedBytes(2, ">H")

    def get16Signed(self):
        global connection

        try:
            return struct.unpack(">h", connection.read(2))[0]
        except serial.SerialException:
            print("Lost connection")
            connection = None
        except struct.error:
            print("Got unexpected data from serial port.")
            return None

    def getDecodedBytes(self, n, fmt):
        global connection
        #print(connection.read(n))
        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print("Lost connection")
            connection = None
            return None
        except struct.error:
            print("Got unexpected data from serial port.")
            return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
