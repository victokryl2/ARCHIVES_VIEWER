from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import Qt

import f_br


class FileBrowser(QtWidgets.QMainWindow, f_br.Ui_MainWindow):
    def __init__(self, mainwind, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш f_br.py
        self.setWindowTitle("Выбор файла для анализа")
        self.mainwind = mainwind

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

        # 1) добавляем виджет в список архивов rgb(138, 191, 255)
        # self.dummy_widget = QtWidgets.QWidget()
        # self.dummy_widget.setFixedSize(40, 20)
        # self.dummy_widget.setStyleSheet("background-color: rgb(138, 191, 255)")
        
        # self.mainwind.scrollArea.setWidget(self.dummy_widget)


        # 1,5) сворачиваем файл-браузер
        self.mainwind.fb.close()

        # 2) читаем файл в pandas.frame

        # 3) проверяем и подготавливаем данные

        # 4) выбираем сколько графиков будем строить

        # 5) строим графики и легенду на вкладке Графики



        # # нижеследующие 3 строчки открывают файл для просмотра
        # index = self.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        # file_path = self.model.filePath(index)  # получаем по этому индексу путь к объекту
        # os.startfile(file_path)


