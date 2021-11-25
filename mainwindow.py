
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
import pandas as pd
import os

import interface
import filebrowser
import globals
import main_dataframe
import graphic
import legend

# Класс главного окна со своим конструктором
class MainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш interface.py
        self.setWindowTitle("Просмоторщик архивов данных")
        
        self.w_height = 0   # высота главного виджета (от него считается высота легенды)

        # коннект на нажатие кнопки Обновить
        self.pushButton.clicked.connect(self.on_button_obnovit)
        # коннект на клик вкладки Графики
        self.tabWidget.tabBarClicked.connect(self.on_tab_click)

        # формируем скролэрию с ф-ией Drags&Drop в разделе Активные архивы
        self.scr_area = SubScrollAr(self)                       # создаём объект скролэрии
        self.verticalLayout_3.addWidget(self.scr_area)          # помещаем скролэрию в layout виджета верхнего уровня
        self.lay_a = QVBoxLayout()                              # lay внутрь скролэрии
        self.scr_area.setLayout(self.lay_a)                     # устанавливаем lay внутрь скролэрии
        self.lay_a_1 = QVBoxLayout()                            # lay_1 внутрь lay
        self.lay_a.addLayout(self.lay_a_1)                      # устанавливаем lay_1 в lay
        self.dummy_widget = SubWidget(self, self)               # вспомогательный виджет внутри lay_2
        self.lay_a.addWidget(self.dummy_widget)                 # добавляем dummy_widget в lay_2

        # формируем скролэрию с ф-ией Drags&Drop в разделе Активные параметры
        self.scr_area2 = SubScrollAr2(self)                      # создаём объект скролэрии
        self.verticalLayout_5.addWidget(self.scr_area2)          # помещаем скролэрию в layout виджета верхнего уровня
        self.lay_b = QVBoxLayout()                               # lay внутрь скролэрии
        self.scr_area2.setLayout(self.lay_b)                     # устанавливаем lay внутрь скролэрии
        self.lay_b_1 = QVBoxLayout()                             # lay_1 внутрь lay
        self.lay_b.addLayout(self.lay_b_1)                       # устанавливаем lay_1 в lay
        self.dummy_widget2 = SubWidget2(self, self)              # вспомогательный виджет внутри lay_2
        self.lay_b.addWidget(self.dummy_widget2)                 # добавляем dummy_widget в lay_2

    # метод коннекта на нажатие кнопки "Обновить"
    def on_button_obnovit(self):
        self.fb = filebrowser.FileBrowser(self) # объект файл-браузера
        self.fb.show()

    # метод коннекта на нажатие вкладки "Графики"
    def on_tab_click(self, index):
        if index == 2:
            # синтезируем главную датафрейм
            main_df = main_dataframe.MainDataframe(self)
            # строим графики и легенду на вкладке Графики
            self.graphic = graphic.Graphic(self)    # создаём объект класса Graphic
            # строим легенду
            self.legend = legend.Legend(self, self.graphic)

    # переопределим метод событий mainwindow с целью определения его размеров
    # и регулирования высоты виджета с легендой
    def resizeEvent(self, event):         
        self.wheight = self.size().height()   # определили высоту mainwindow


#####################################################################################
####### ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ  #####################################################
#####################################################################################

# @brief  Класс объекта скроллэрии раздела Активные архивы
# @detail Этот класс создан для переопределения методов для работы Drag&Drop и придания его объектам необходимых свойств
# @param  mainwindow - объект главного окна интерфейса
# @retval None 
class SubScrollAr(QScrollArea):
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
        self.button.setStyleSheet("background-color: rgb(134, 182, 255)")
        self.button.setText(e.mimeData().text())
        self.mainwind.lay_1.addWidget(self.button)

# @brief  Класс объекта скроллэрии "2"
# @detail Этот класс создан для переопределения методов для работы Drag&Drop и придания его объектам необходимых свойств
# Данный класс SubScrollAr2 отличается от SubScrollAr тем, что по dropevent-у создаются Лейблы, а не кнопки.
# @param  mainwindow - объект главного окна интерфейса
# @retval None 
class SubScrollAr2(QScrollArea):
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
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label.setMinimumHeight(35)
        self.label.setStyleSheet("background-color: rgb(134, 182, 255)")
        self.label.setText(e.mimeData().text())
        self.mainwind.lay_b_1.addWidget(self.label)
        

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

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.button1 = QPushButton()
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button1.setMinimumHeight(35)
        self.button1.setStyleSheet("background-color: rgb(134, 182, 255)")
        self.button1.setText(e.mimeData().text())
        self.mainwind.lay_a_1.addWidget(self.button1)
        # коннект на клик выбранного архива в разделе Активные архивы
        self.button1.clicked.connect(self.on_button_achive)

    # метод нажатия на кнопку архива, который был добавлен в раздел Активные архивы
    def on_button_achive(self):
        # извлекаем id объекта (в данном случае это у нас название архива),
        # что является ключом для поиска в словаре
        sender = self.sender()  # получаем id экземпляра
        key = sender.text()     # получаем из экземпляра текст
        # помещаем название архива в промежут. переменную
        globals.archname_archpath[0] = key
        # извлекаем из словаря соответствующий имени путь и помещаем в промежут. переменную
        globals.archname_archpath[1] = globals.arch_dict[key]

        dir_path = globals.archname_archpath[1]
        objects_list = os.listdir(dir_path)           # получаем список имён всех объектов папки

        # ищем первый попавшийся файл csv и получаем из него список параметров
        for i in range(len(objects_list)):
            if objects_list[i].endswith('csv'):
                obj_path = os.path.join(dir_path, objects_list[i])   # соединяем путь к папке объекта с именем объекта
                dataframe = pd.read_csv(obj_path)                    # читаем данные из csv в dataframe
                names = dataframe.columns.tolist()                   # получаем список имён колонок (список параметров)
                break
            else:
                print('false')

        # загружаем список параметров в раздел Все параметры архива
        self.clearLayout(self.mainwind.verticalLayout_10)   # предварительно очищаем от старых значений
        for i in range(len(names)):
            self.label1 = SubDragsLabel()
            self.label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.label1.setMinimumHeight(20)
            self.label1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.label1.setStyleSheet("background-color: rgb(134, 182, 255)")
            self.label1.setText('  ' + names[i])
            self.mainwind.verticalLayout_10.addWidget(self.label1)

    # метод, очищающий лейоут от всего содержимого
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


# @brief  Класс объекта вспомогательного виджета для раздела Активные параметры
# @detail Обладая политикой expanding объект этого класса, расширяясь в вертикальном направлении,
# заставляет быть добавляемые объекты всегда вверху.
# Этот класс SubWidget2 отличается от класса SubWidget тем, добавляет лейблы в
# @param  mainwindow - объект главного окна интерфейса
# @retval None 
class SubWidget2(QWidget):
    def __init__(self, mainwindow, parent):
        super().__init__(parent)
        self.mainwind = mainwindow
        self.setAcceptDrops(True)   # разрешаем виджету принимать действие drop
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.label2 = QLabel()
        self.label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label2.setMinimumHeight(35)
        self.label2.setStyleSheet("background-color: rgb(134, 182, 255)")
        # почему-то в процессе переноса чарез mime добавляются два пробела впереди
        # нижеследующие 2 строчки удаляют эти 2 пробела
        tmp_text = e.mimeData().text()
        new_text = tmp_text.replace(' ', '', 2)
        self.label2.setText('['+ globals.archname_archpath[0] +']' + ' *' + new_text)
        self.mainwind.lay_b_1.addWidget(self.label2)


# @brief  Класс создания объектов label с ф-ией Drags&Drop
# @detail При помощи этого класса создаются labels в классе class HL(QtWidgets.QWidget)
# @param  None
# @retval None       
class SubDragsLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

    # переопределяем метод нажатия кнопки
    def mousePressEvent(self, e):
        mimeData = QMimeData()          # создаём объект mimdata
        mimeData.setText(self.text())   # помещаем туда информацию (текст лейбла)
        drag = QDrag(self)              # создаём объект drag
        drag.setMimeData(mimeData)      # помещаем туда mimdata
        drag.exec()                     # запускаем drag&drop









        
        





        
