
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import random

# отдельный класс для линий
class Lines(QWidget):
    def __init__(self, rgb, parent=None): # конструктор класса Lines
        QWidget.__init__(self, parent=parent)   # конструктор родительского класса

        self.rgb = rgb                          # элемент из списка цветов (кортеж из 3-х)
        self.line_y_coord = 11                   # координата "y" линий
        
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
    def __init__(self, mainwindow, graphic, parent=None): # конструктор класса Legend
        QWidget.__init__(self, parent=parent)   # конструктор родительского класса

        self.mainwind = mainwindow
        self.graphic = graphic
        self.lines_list = []               # список для хранения объектов линий
        self.graph_names = []

        # получаем список объектов Qlabel с текстом названий актуальных графиков
        self.graph_names = self.get_lines_names()
        
        # создаём массив объектов класса линий Lines()
        # во время итерации каждый раз передаём туда очередной
        # цвет из списка цветов из модуля grafic
        for i in range(len(self.graphic.colors_list)):
            self.lines_list.append(Lines(self.graphic.colors_list[i]))

        # создаём QGridLayout (для размещения потом на нижнем виджете)
        self.grid = QGridLayout()               # объект контейнера
        self.grid.setColumnMinimumWidth(0, 50)  # минимальная ширина 0-го столбца
        self.grid.setColumnStretch(2, 1)        # растяжение второго столбца с коэффициентом 1
        self.grid.setColumnStretch(3, 10)       # растяжение третьего столбца с коэффициентом 10

        ###############################################################################################
        # формируем рандомный список объектов чисел курсора
        self.vals_list = []
        for i in range(len(self.lines_list)):
            label = QLabel()
            label.setFont(QtGui.QFont('Arial', 12))
            self.vals_list.append(label)
            val = random.uniform(-10, 10)
            val = round(val, 2)
            self.vals_list[i].setNum(val)
            self.vals_list[i].setAlignment(Qt.AlignCenter)

        ###############################################################################################

        # добавляем туда новые объекты
        for i in range(len(self.lines_list)):
            self.grid.addWidget(self.lines_list[i], i, 0)
            self.grid.addWidget(self.vals_list[i], i, 2)   
            self.grid.addWidget(self.graph_names[i], i, 3)
        
        # Установка V-контейнера на виджет.
        # Внимание! Есть механизм регулирования высоты виджета от кол-ва строк легенды.
        # Это переопределяемый метод, находящийся в mainwindow.py.
        self.mainwind.widget_6.setLayout(self.grid)
        self.w_edjustment()  # регулируем высоту легенды   


    #################################################################################################
    ####### МЕТОДЫ ##################################################################################
    #################################################################################################

    # @brief  Метод регулировки высоты легенды
    # @detail Была проблема - при малом кол-ве строк легенды они плохо отбражались 
    # на виджете. Этот метод позволяет избежать этой проблемы сразу привязывая 
    # высоту виджета к размеру окна и кол-ву строк.
    # @param  None
    # @retval None
    def w_edjustment(self):
        maxheight = self.mainwind.w_height/3            # задали максимальную высоту виджета относительно mainwindow
        # регулируем высоту виджета 2 согласно количеству графиков
        n = len(self.lines_list)
        minh = n * 20
        if (minh < 30):
            minh = 30
        if (minh > maxheight):
            minh = maxheight
        if (n == 2):
            minh = 60    
        self.mainwind.widget_6.setMinimumHeight(minh)

    # @brief  Метод получения списка названий линий легенды, соответствующего отображаемым графикам.
    # @detail Сначала из dataframe получается список наименований всех колонок,
    # потом оттуда выбираются нужные. Далее в итератора создаются объекты QLabel и туда записываются названия графиков.
    # Из объектов QLabel составляется список. Метод возвращает список объектов QLabel с нужным текстом в них.
    # @param  None
    # @retval None
    def get_lines_names(self):
        # Создание списка названий колонок (будущие названия графиков в легенде)
        actual_names = []    # список актуальных названий линий легенды
        for i in self.graphic.col_names:
            label = QLabel()
            label.setFont(QtGui.QFont('Arial', 12))
            label.setText(i)
            actual_names.append(label)
        return actual_names
