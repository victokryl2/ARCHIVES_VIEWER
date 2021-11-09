from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import f_br
import data
import graphic

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
        # # нижеследующие 3 строчки открывают файл для просмотра (НЕ УДАЛЯТЬ! ЭТО ПОЛЕЗНО!)
        # index = self.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        # file_path = self.model.filePath(index)  # получаем по этому индексу путь к объекту
        # os.startfile(file_path)

        # 1) добавляем виджет с именем открытого архива в поле Список архивов
        self.hl = HL()
        self.mainwind.verticalLayout_8.addWidget(self.hl)

        # 2) сворачиваем файл-браузер
        self.mainwind.fb.close()

        # 3) читаем файл в pandas.frame
        self.data = data.Data(self)                 # создаём объект класса Data

        # 4) строим графики и легенду на вкладке Графики
        self.graphic = graphic.Graphic(self.mainwind, self.data)    # создаём объект класса Graphic
        


# @brief  Класс создания кастомизированных объектов "выбранный архив" для вкладки Список архивов.
# @detail Создаёт виджет, содержащий H-контейнер, который используется для размещения лейбла 
# с названием архива по центру. Справа и слева от лейбла добавляются вспомогательные виджеты,
# которые и центрируют лейбл визуально по центру раздела.
# @param  None
# @retval None       
class HL(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel('ВАГОН №5')
        self.label.setFixedSize(100, 100)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label.setStyleSheet("background-color: rgb(138, 191, 255)")

        self.widget1 = QtWidgets.QWidget()
        self.widget2 = QtWidgets.QWidget()

        self.hlay = QtWidgets.QHBoxLayout(self)

        self.hlay.addWidget(self.widget1)
        self.hlay.addWidget(self.label)
        self.hlay.addWidget(self.widget2)






