
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

# отдельный класс для линий
class Lines(QWidget):
    def __init__(self, rgb, parent=None): # конструктор класса Lines
        QWidget.__init__(self, parent=parent)   # конструктор родительского класса

        self.rgb = rgb                          # элемент из списка цветов (кортеж из 3-х)
        self.line_y_coord = 7                   # координата "y" линий
        
    def paintEvent(self, e):                    # переопределяем метод paintEvent
        self.qp = QPainter()
        self.qp.begin(self)
        self.drawLines(self.qp)
        self.qp.end()

    def drawLines(self, qp):
        self.pen = QPen(QColor(self.rgb[0], self.rgb[1], self.rgb[2]), 2, Qt.SolidLine)
        self.qp.setPen(self.pen)
        self.qp.drawLine(10, self.line_y_coord, 100, self.line_y_coord)

class Legend(QWidget):
    def __init__(self, mainwindow, parent=None): # конструктор класса Lines
        QWidget.__init__(self, parent=parent)   # конструктор родительского класса

        self.mainwindow = mainwindow
        self.num = self.mainwindow.data.n  # кол-во объектов легенды
        self.lines_list = []               # список для хранения объектов линий

        # создаём массив объектов класса линий Lines()
        # во время итерации каждый раз передаём туда очередной
        # цвет из списка цветов из модуля grafics
        for i in range(self.num):
            # self.lines_list.append(Lines(self.mainwindow.data.col_list_of_tuples[i]))
            self.lines_list.append(Lines(self.mainwindow.graphic.colors_list[i]))

        # создаём QGridLayout на нижнем виджете
        self.grid = QGridLayout()               # объект контейнера
        self.grid.setColumnMinimumWidth(0, 50)  # миниммальная ширина 0-го столбца
        self.grid.setColumnStretch(2, 1)        # растяжение второго столбца с коэффициентом 1
        self.grid.setColumnStretch(3, 10)       # растяжение третьего столбца с коэффициентом 10

        # добавляем туда новые объекты
        for i in range(self.num):
            self.grid.addWidget(self.lines_list[i], i, 0)
            self.grid.addWidget(self.mainwindow.data.vals_list[i], i, 2)   
            self.grid.addWidget(self.mainwindow.data.graph_names[i], i, 3)
        
        # установка V-контейнера на виджет
        self.mainwindow.widget_2.setLayout(self.grid)       