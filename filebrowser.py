import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag

import f_br
import data
import graphic
import legend
import globals

# @brief  Класс создания файлового браузера.
# @detail Этот файловый браузер нужен для выбора папки с интересующим архивом.
# @param  None
# @retval None 
class FileBrowser(QtWidgets.QMainWindow, f_br.Ui_MainWindow):
    def __init__(self, mainwind, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш f_br.py
        self.setWindowTitle("Выбор файла для анализа")
        self.mainwind = mainwind
        self.archive_name = ''

        # последующие 2-е строки инициализируют (или разрешают) показывать
        # контектное меню по правой кнопке мыши
        # включаем эмитирование сигнала запроса контекстного меню: QWidget::customContextMenuRequested()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # коннект на сигнал QWidget::customContextMenuRequested()
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        self.populate()

    # метод, создающий окно браузера с содержимым в "точке входа"
    def populate(self):
        # в этом абзаце кода формируется браузер с точкой входа самого высокого уровня - 
        # начиная со списка дисков
        self.model = QtWidgets.QFileSystemModel()        # создаём объект модели браузера
        self.model.setRootPath(QtCore.QDir.rootPath())   # устанавливаем стандартный rootPath самого высокого уровня (начиная со списка дисков)
        self.treeView.setModel(self.model)               # устанавливаем модель в виджет "treeView"

        # если нужна другая точка входа, то нужно задать точку входа и передать её
        # объекту "treeView"
        # path = 'D:'                                 # точка входа браузера (откуда начнётся просмотр)
        # self.treeView.setRootIndex(self.model.index(path))

        # инициализация сортировки в колонках браузера (по дате, по размеру)
        self.treeView.setSortingEnabled(True)

    # метод для коннекта по правой кнопке мыши, который формирует меню действий с файлом
    def context_menu(self):
        menu = QtWidgets.QMenu()                # создаём объект меню
        open = menu.addAction('Open')           # объект действия по пункту меню "Open"
        open.triggered.connect(self.open_file)  # коннект триггера по меню open с методом open_file() обработки пункта меню

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


##############################################################################################################
################## МЕТОДЫ ####################################################################################
##############################################################################################################
    
    # @brief  Метод коннекта на нажатие кнопки Open файл-браузера
    # @detail Метод определяет только папки в данной директории (при помощи метода get_subdirs_list())
    # и помещает их имена в раздел Список архивов.
    # @param  None
    # @retval None 
    def open_file(self):
        # # нижеследующие 3 строчки открывают файл для просмотра (НЕ УДАЛЯТЬ! ЭТО ПОЛЕЗНО!)
        # index = self.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        # file_path = self.model.filePath(index)  # получаем по этому индексу путь к объекту
        # os.startfile(file_path)

        # получаем список имён всех объектов папки
        index = self.treeView.currentIndex()            # получаем индекс директории
        self.dir_path = self.model.filePath(index)      # получаем по индексу путь к папке
        self.objects_list = os.listdir(self.dir_path)   # получаем список имён всех объектов папки

        # получаем список только поддиректорий (файлы будут игнорироваться)
        self.subdirs_list = self.get_subdirs_list()

        # помещаем перечень папок в раздел Список архивов
        for i in range(len(self.subdirs_list)):
            hl = HL(self.subdirs_list[i])
            self.mainwind.verticalLayout_8.addWidget(hl)

        # 2) сворачиваем файл-браузер
        self.mainwind.fb.close()

        # 3) читаем файл в pandas.frame
        self.data = data.Data(self)                                 # создаём объект класса Data
        
        # # 4) строим графики и легенду на вкладке Графики
        # self.graphic = graphic.Graphic(self.mainwind, self.data)    # создаём объект класса Graphic
        # # 5) строим легенду
        # self.legend = legend.Legend(self.mainwind, self.graphic)



    # @brief  Метод получения списка архивов в корневой папке
    # @detail Метод создаёт словарь "имя_архива -> "
    # и помещает их имена в раздел Список архивов.
    # @param  None
    # @retval None
    def get_subdirs_list(self):
        # получаем список только поддиректорий (файлы будут игнорироваться)
        objects_list = os.listdir(self.dir_path)           # получаем список имён всех объектов папки
        sub_directories = []                               # список для путей
        for item in objects_list:                          # будут перебираться все объекты папки (папки и файлы)
            obj_path = os.path.join(self.dir_path, item)   # соединяем путь к папке объекта с именем объекта

            if os.path.isdir(obj_path):                     # проверяем, является ли объект папкой, если является, то:
                dir_name = os.path.basename(obj_path)       # обратно отделяем имя папки от пути
                globals.arch_dict[dir_name] = obj_path      # добавляем путь и имя в словарь
                sub_directories.append(dir_name)            # добавляем имя архива в список
        print(globals.arch_dict)
        return sub_directories



# @brief  Класс создания кастомизированных объектов "выбранный архив" для вкладки Список архивов.
# @detail Класс HL (Horizontal Layout) cоздаёт виджет, содержащий H-контейнер, который используется для размещения лейбла 
# с названием архива по центру. Справа и слева от лейбла добавляются вспомогательные виджеты,
# которые и центрируют лейбл визуально по центру раздела.
# @param  None
# @retval None       
class HL(QtWidgets.QWidget):
    def __init__(self, archive_name):
        super().__init__()
        self.archive_name = archive_name

        self.label = DragsLabel(self.archive_name)
        self.label.setFixedSize(100, 100)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label.setStyleSheet("background-color: rgb(138, 191, 255)")

        self.widget1 = QtWidgets.QWidget()
        self.widget2 = QtWidgets.QWidget()

        self.hlay = QtWidgets.QHBoxLayout(self)

        self.hlay.addWidget(self.widget1)
        self.hlay.addWidget(self.label)
        self.hlay.addWidget(self.widget2)

# @brief  Класс создания объектов label с ф-ией Drags&Drop
# @detail При помощи этого класса создаются labels в классе class HL(QtWidgets.QWidget)
# @param  None
# @retval None       
class DragsLabel(QtWidgets.QLabel):
    def __init__(self, archive_name):
        super().__init__(archive_name)
        self.archive_name = archive_name
        self.setText(self.archive_name)

    # переопределяем метод нажатия кнопки
    def mousePressEvent(self, e):
        mimeData = QMimeData()          # создаём объект mimdata
        mimeData.setText(self.text())   # помещаем туда информацию
        drag = QDrag(self)              # создаём объект drag
        drag.setMimeData(mimeData)      # помещаем туда mimdata
        drag.exec()                     # запускаем drag&drop





