from PyQt5 import QtWidgets


class TimerLCDNumber(QtWidgets.QLCDNumber):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLCDNumber.__init__(self, *args, **kwargs)

    def setValue(self, value):
        self.display(value)

    def noConnection(self):
        self.timer.stop()