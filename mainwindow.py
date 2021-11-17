
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
import pandas as pd
import os

import interface
import filebrowser
import globals

# Класс главного окна со своим конструктором
class MainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш interface.py
        self.setWindowTitle("Просмоторщик архивов данных")
        
        self.w_height = 0   # высота главного виджета (от него считается высота легенды)

        # коннект на нажатие кнопки Обновить
        self.pushButton.clicked.connect(self.on_button)

        self.scr_area = ScrollAr(self)                          # создаём объект скролэрии
        self.verticalLayout_3.insertWidget(1, self.scr_area)    # помещаем скролэрию в layout виджета верхнего уровня

        self.lay = QVBoxLayout()                                # lay внутрь скролэрии
        self.scr_area.setLayout(self.lay)                       # устанавливаем lay внутрь скролэрии
        self.lay_1 = QVBoxLayout()                              # lay_1 внутрь lay
        self.lay.addLayout(self.lay_1)                          # устанавливаем lay_1 в lay
        

        self.dummy_widget = SubWidget(self, self)               # вспомогательный виджет внутри lay_2
        self.lay.addWidget(self.dummy_widget)                 # добавляем dummy_widget в lay_2






    def on_button(self):
        self.fb = filebrowser.FileBrowser(self) # объект файл-браузера
        self.fb.show()

    ####### ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ #################################################
    #################################################################################

    # переопределим метод событий mainwindow с целью определения его размеров
    # и регулирования высоты виджета с легендой
    def resizeEvent(self, event):         
        self.wheight = self.size().height()   # определили высоту mainwindow


#####################################################################################
####### ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ  #####################################################
#####################################################################################

# @brief  Класс объекта скроллэрии
# @detail Этот класс создан для переопределения методов для работы Drag&Drop придания его объектам необходимых свойств
# @param  mainwindow - объект главного окна интерфейса
# @retval None 
class ScrollAr(QScrollArea):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwind = mainwindow
        self.setAcceptDrops(True)
    # переопределяем метод перехода границы виджета
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()
    # переопределяем метод события drop
    def dropEvent(self, e):
        self.button = QPushButton(self)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button.setMinimumHeight(35)
        self.button.setStyleSheet("background-color: rgb(138, 191, 255)")
        self.button.setText(e.mimeData().text())
        self.mainwind.lay_1.addWidget(self.button)
        

# @brief  Класс объекта вспомогательного виджета
# @detail Обладая политикой expanding объект этого класса расширяясь в вертикальном направлении
# заставляет быть добавляемые объекты всегда вверху
# @param  mainwindow - объект главного окна интерфейса
# @retval None 
class SubWidget(QWidget):
    def __init__(self, mainwindow, parent):
        super().__init__(parent)
        self.mainwind = mainwindow
        self.setAcceptDrops(True)   # разрешаем виджету принимать действие drop
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: rgb(138, 191, 255)")

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button.setMinimumHeight(35)
        self.button.setStyleSheet("background-color: rgb(138, 191, 255)")
        self.button.setText(e.mimeData().text())
        self.mainwind.lay_1.addWidget(self.button)
        # коннект на клик выбранного архива в разделе Активные архивы
        self.button.clicked.connect(self.on_button)

    def on_button(self):
        # извлекаем id объекта (в данном случае это у нас название архива),
        # что является ключом для поиска в словаре
        sender = self.sender()  # получаем id экземпляра
        key = sender.text()     # получаем из экземпляра текст
        # помещаем название архива в промежут. переменную
        globals.archname_archpath[0] = key
        # извлекаем из словаря соответствующий имени путь и помещаем в промежут. переменную
        globals.archname_archpath[1] = globals.arch_dict[key]
        print(globals.archname_archpath)

        dir_path = globals.archname_archpath[1]
        objects_list = os.listdir(dir_path)           # получаем список имён всех объектов папки
        print(objects_list)

        # ищем первый попавшийся файл csv и получаем из него список параметров
        for i in range(len(objects_list)):
            if objects_list[i].endswith('csv'):
                obj_path = os.path.join(dir_path, objects_list[i])   # соединяем путь к папке объекта с именем объекта
                dataframe = pd.read_csv(obj_path)                    # читаем данные из csv в dataframe
                names = dataframe.columns.tolist()                   # получаем список имён колонок (список параметров)
                break
            else:
                print('false')
        print(names)

        # загружаем список параметров в раздел Все параметры архива
        # for i in range(len(names)):

        #     self.button1 = QPushButton()
        #     self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        #     self.button1.setMinimumHeight(20)
        #     self.button1.setAlignment(Qt.AlignHLeft | Qt.AlignVCenter)
        #     self.button1.setStyleSheet("background-color: rgb(138, 191, 255)")
        #     self.button1.setText(names[i])
        #     self.mainwind.verticalLayout_10.addWidget(self.button1)
        #     # коннект на клик выбранного архива в разделе Активные архивы
        #     # self.button.clicked.connect(self.on_button1)





        
        





        
