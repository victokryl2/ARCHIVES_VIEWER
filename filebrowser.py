from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import os

import f_br


class FileBrowser(QtWidgets.QMainWindow, f_br.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш f_br.py
        self.setWindowTitle("Выбор файла для анализа")

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

    # метод действия по клику по пункту меню "Open"
    def open_file(self):
        index = self.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        file_path = self.model.filePath(index)  # получаем по этому индексу путь к объекту
        os.startfile(file_path)


