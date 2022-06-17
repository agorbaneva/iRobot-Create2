from PyQt5 import QtCore, QtWidgets, QtGui

class HighlightEffect(QtWidgets.QGraphicsEffect):
    def __init__(self, offset=1.5, parent=None):
        super(HighlightEffect, self).__init__(parent)
        self._color = QtGui.QColor(159, 143, 212)
        self._offset = offset * QtCore.QPointF(1, 1)

    @property
    def offset(self):
        return self._offset

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    def boundingRectFor(self, sourceRect):
        return sourceRect.adjusted(
            -self.offset.x(), -self.offset.y(), self.offset.x(), self.offset.y()
        )

    def draw(self, painter):
        offset = QtCore.QPoint()
        try:
            pixmap = self.sourcePixmap(QtCore.Qt.LogicalCoordinates, offset)
        except TypeError:
            pixmap, offset = self.sourcePixmap(QtCore.Qt.LogicalCoordinates)

        bound = self.boundingRectFor(QtCore.QRectF(pixmap.rect()))
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.color)
        p = QtCore.QPointF(offset.x() - self.offset.x(), offset.y() - self.offset.y())
        bound.moveTopLeft(p)
        painter.drawRoundedRect(bound, 5, 5)
        painter.drawPixmap(offset, pixmap)
        painter.restore()
