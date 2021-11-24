import matplotlib.pyplot as plt
# plt.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

import globals


# Пользовательский класс, наследованный от FigureCanvas.
# В нём собраны все методы, необходимые для рисования графика.
# Позже график можно создавать просто создав объект этого класса.
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()                          # создание объекта Figure
        # регулируем границы зоны subplot (максимально растягиваем график на виджете)
        self.fig.subplots_adjust(left=0.04, right=0.99, top=0.99, bottom=0.1)
        self.axes = self.fig.add_subplot()           # создание самого графика
        super(MplCanvas, self).__init__(self.fig)    # создание объекта холста
        

class Graphic(QWidget):
    def __init__(self, mainwindow, datasource, parent=None):# конструктор класса Grafic
        QWidget.__init__(self, parent=parent)   # конструктор родительского класса

        self.mainwind = mainwindow
        # self.data = datasource.data
        self.data = globals.main_df
        print(self.data)
        self.column_list = [1]      # список колонок, по которым графики строить
        self.colors_list = []           # список для хранения кодов цветов линий легенды

        # Создание объекта графика как объекта пользовательского класса MplCanvas
        self.main_graph = MplCanvas()
        self.col_names = self.data.columns.tolist()
        for i in self.column_list:
            self.y = self.data[self.col_names[i]]
            x = list(range(len(self.y)))
            self.main_graph.axes.plot(x, self.y, label = 'dummy_text')
        # чтобы графики начинались от оси х
        self.main_graph.axes.set_xlim(xmin = x[0], xmax = x[(len(self.y) -1)])
        self.main_graph.axes.grid() # включаем сетку

        #############  ПОЛУЧЕНИЕ СПИСКА ЦВЕТОВ ЛЕГЕНДЫ В ФОРМАТЕ RGB ##################################
        # Этот список будет использоваться для построения пользовательской легенды в модуле legend.py
        self.legend = self.main_graph.axes.legend()    # создаём объект легенды
        self.lines = self.legend.get_lines()   # получаем объекты линий легенды (массив объектов)
        for i in range(len(self.lines)):
            hex = self.lines[i].get_color()    # получаем цветовой код линии в формате #2ca02c
            hex = hex.replace('#', '')         # убираем знак #
            # метод hex_to_rgb() преобразует шестизначный hex в список rgb из 3-х чисел int,
            # а метод append добавляет этот элементарный список в полный список кодов rgb
            self.colors_list.append(self.hex_to_rgb(hex))
        self.legend.set_visible(False) # делаем легенду невидимой
        ################################################################################################

        # создание объекта панели навигации на холсте self.main_graph
        self.toolbar = NavigationToolbar(self.main_graph, self)
        # Cоздание вертикального контейнера VB-Layout и помещение туда панели навигации и фигуры.
        # Порядок важен. Если сначала добавить main_graph, то панель навигации окажется внизу.
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.main_graph)
        
        # установка контейнера Layout в нужный виджет
        self.mainwind.widget_3.setLayout(self.layout)

    def hex_to_rgb(self, hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        return rgb