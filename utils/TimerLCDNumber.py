from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimerEvent


class TimerLCDNumber(QtWidgets.QLCDNumber):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLCDNumber.__init__(self, *args, **kwargs)
        # self.timer = QtCore.QTimer(self)
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.onTimeout)
        # self.finished = self.value()

    # def timerEvent(self, event:QTimerEvent):
    #    if self._timerId!=event.timerId(): return
    #    self.setValue(self.finished)

    def setValue(self, value):
        # self._timerId = self.startTimer(1000)
        self.display(value)
        # self.finished = value
        # self.timer.start()

    # def onTimeout(self):
    #     current = self.value()
    #     if self.finished != current:
    #         count = 1 if self.finished > current else -1
    #         self.display(current + count)
    #     self.timer.stop()
    #     self.timer.start()

    def noConnection(self):
        self.timer.stop()