from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsView
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect
import numpy as np


class MouseDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.show()

        self.update()


    def paintEvent(self, event):

        #print(self.points)

        painter = QPainter()
        painter.begin(self)

        painter.drawEllipse(self.geometry().width()//2 - 30/2, self.geometry().height()//2 - 30/2, 30, 30)

        if len(self.points) > 1:
            for x in range(len(self.points)-1):
                painter.drawLine(self.points[x][0], self.points[x][1], self.points[x+1][0], self.points[x+1][1])

        self.followPath()
        painter.end()

    def mousePressEvent(self, event):
        if self.points == []:
            if event.buttons() and Qt.LeftButton:
                self.points = [[self.geometry().width()//2, self.geometry().height()//2]]

    def mouseReleaseEvent(self, event):
        self.points += [[event.pos().x(), event.pos().y()]]
        self.update()

    def followPath(self):
        if len(self.points) < 2:
            return []

        center = self.points[0]

        movements = {}
        for x in range(len(self.points) - 1):

            [x1, y1], [x2, y2] = self.points[x], self.points[x+1]
            distance =  ( (x1-x2)**2 + (y1-y2)**2 ) ** (1/2)

            # for the very first line, compare it to a straight line

            if movements == {}:
                vector1 = [x2 - center[0], y2 - center[1]]
                vector2 = [0, -1]

                turn_angle = self.calculateAngle(vector1, vector2)
                turn_angle = 180 - turn_angle
                direction = self.turnWhichWay([0, 0], [0, 1], vector1)
                movements[x] = [distance, turn_angle, direction]
                continue

            # otherwise, create two vectors comparing to the middle point as the new origin
            vector1 = [x1-x2, y1-y2]
            vector2 = [x1 - self.points[x-1][0], y1-self.points[x-1][1]]

            turn_angle = self.calculateAngle(vector1, vector2)
            direction = self.turnWhichWay([0, 0], vector2, vector1)
            movements[x] = [distance, turn_angle, direction]

        return movements

    def calculateAngle(self, vector1, vector2):

        unit_vector_1 = vector1 / np.linalg.norm(vector1)
        unit_vector_2 = vector2 / np.linalg.norm(vector2)
        #dot_product = np.dot(unit_vector_1, unit_vector_2)

        angle = np.arccos(np.clip(np.dot(unit_vector_1, unit_vector_2), -1.0, 1.0))

        # angle in degrees
        angle *= 180 / np.pi
        turn_angle = 180 - angle
        return turn_angle

    def turnWhichWay(self, segment_p1, segment_p2, point):
        # determine which side of the segment the point is on
        # so robot can turn left or right
        dot = (point[0] - segment_p1[0])*(segment_p2[1] - segment_p1[1]) - (point[1] - segment_p1[1])*(segment_p2[0] - segment_p1[0])
        if dot < 0:
            return "L"
        if dot > 0:
            return "R"
        else:
            return 0

    def clearLines(self):
        self.points = []
        self.update()