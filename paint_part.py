from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class My_Board(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_length = 905
        self.pixmap_wigth = 515
        self.pixmap = QPixmap(self.pixmap_length, self.pixmap_wigth)
        self._IfEmpty = 1
        self.Draw = "线"
        self.pixmap.fill(Qt.white)
        self.setStyleSheet("border: 1px solid black")
        self.Color = Qt.black
        self.pen_width = 1
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.start = QPoint()
        self.stop = QPoint()
        self.situation1 = False
        self.shape1 = None
        self.rect_list = []
        self.situation2 = False
        self.shape2 = None
        self.ellipse_list = []
        self.pos_xy = []
        self.points = []
        self.points_up = []  # 储存读取的坐标点
        self.points_xie = []
        self.points_cir = []
        self.drawpath = False
        self.coord_rect_all = []
        self.coord_elli_all = []
        self.elli_long_all = []
        self.elli_short_all = []
        self.initui()

    def initui(self):
        self.setMouseTracking(False)
        self.setGeometry(500, 300, 100, 25)
        self.setWindowTitle('Event object')
        self.show()

    def make_image(self):
        img = self.pixmap.toImage()
        return img

    def paintEvent(self, event):
        self.painter = QPainter(self)
        size = self.size()
        self.painter.begin(self.pixmap)
        self.painter.drawPixmap(0, 0, self.pixmap)
        self.painter.setPen(QPen(self.Color, self.pen_width, Qt.SolidLine))
        if self.points_cir:
            self.painter.drawEllipse(self.points_cir[0][0], self.points_cir[0][1],
                                     self.points_cir[1][0] - self.points_cir[0][0],
                                     self.points_cir[1][1] - self.points_cir[0][1])
        if self.points_up:
            self.painter.drawPolygon(QPolygon(self.points_up))
        if self.points_xie:
            self.painter.drawPolygon(QPolygon(self.points_xie))

        if self.points:
            self.painter.drawPolygon(QPolygon(self.points))
        if self._IfEmpty == 0:
            self.ellipse_list = []
            self.rect_list = []
            self.coord_rect_all = []
            self.elli_short_all = []
            self.coord_elli_all = []
            self.elli_long_all = []
            self._IfEmpty = 1
        else:
            for self.shape2 in self.ellipse_list:
                self.shape2.paint2(self.painter)
            for self.shape1 in self.rect_list:
                self.shape1.paint1(self.painter)
        self.painter.end()

    def mousePressEvent(self, event):
        self.x1 = event.x()
        self.y1 = event.y()
        if event.button() == Qt.LeftButton:
            if self.Draw == "线":
                self.endPoint = event.pos()
                self.lastPoint = self.endPoint
                self.update()
            elif self.Draw == "椭圆":
                self.shape2 = Ellipse()
                if self.shape2 is not None:
                    self.situation2 = False
                    self.ellipse_list.append(self.shape2)
                    self.shape2.setStart2(event.pos())
                    self.shape2.setEnd2(event.pos())
            elif self.Draw == "矩形":
                self.shape1 = Rectangle()
                if self.shape1 is not None:
                    self.situation1 = False
                    self.rect_list.append(self.shape1)
                    self.shape1.setStart1(event.pos())
                    self.shape1.setEnd1(event.pos())
                self.update()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        window = self.parent().window()
        if window is not None:
            self.parent().window().Board_Coordinates.setText('X: %d; Y: %d' % (event.x(), event.y()))
        self.painter.begin(self.pixmap)
        self.painter.setPen(QPen(self.Color, self.pen_width, Qt.SolidLine))
        if self.Draw == "线":
            self.endPoint = event.pos()
            self.painter.drawLine(self.lastPoint, self.endPoint)
            self.lastPoint = self.endPoint
            self.update()
        elif self.Draw == "椭圆":
            if self.shape2 is not None and not self.situation2:
                self.shape2.setEnd2(event.pos())
                self.update()
        elif self.Draw == "矩形":
            if self.shape1 is not None and not self.situation1:
                self.shape1.setEnd1(event.pos())
                self.update()
        self.painter.end()

    def mouseReleaseEvent(self, event):
        self.x2 = event.x()
        self.y2 = event.y()
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            if self.Draw == '矩形':
                self.situation1 = True
                self.shape1 = None
                coord_rect = [[self.x1, self.y1], [self.x2, self.y1], [self.x1, self.y2], [self.x2, self.y2]]
                self.coord_rect_all.append(coord_rect)
                print(self.coord_rect_all)
            if self.Draw == '椭圆':
                self.situation2 = True
                self.shape2 = None
                coord_elli = [(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2]
                elli_long = [self.x2, (self.y1 + self.y2) / 2]
                elli_short = abs((self.y1 - self.y2) / 2)
                self.coord_elli_all.append(coord_elli)
                self.elli_long_all.append(elli_long)
                self.elli_short_all.append(elli_short)
                print(self.coord_elli_all)
            self.update()


class Ellipse:
    def __init__(self):
        self.start = QPoint()
        self.end = QPoint()

    def setStart2(self, s):
        self.start = s

    def setEnd2(self, e):
        self.end = e

    def startPoint2(self):
        return self.start

    def endPoint2(self):
        return self.end

    def paint2(self, painter):
        painter.drawEllipse(self.startPoint2().x(), self.startPoint2().y(),
                            self.endPoint2().x() - self.startPoint2().x(),
                            self.endPoint2().y() - self.startPoint2().y())


class Rectangle:
    def __init__(self):
        self.start = QPoint()
        self.end = QPoint()

    def setStart1(self, s):
        self.start = s

    def setEnd1(self, e):
        self.end = e

    def startPoint1(self):
        return self.start

    def endPoint1(self):
        return self.end

    def paint1(self, painter):
        painter.drawRect(self.startPoint1().x(), self.startPoint1().y(), self.endPoint1().x() - self.startPoint1().x(),
                         self.endPoint1().y() - self.startPoint1().y())
