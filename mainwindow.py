
from PyQt5 import QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')

import interface
import filebrowser

# Класс главного окна со своим конструктором
class MainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # загружаем наш interface.py
        self.setWindowTitle("Просмоторщик архивов данных")
        
        self.w_height = 0   # высота главного виджета (от него считается высота легенды)

        # коннект на нажатие кнопки Обновить
        self.pushButton.clicked.connect(self.on_button)

    def on_button(self):
        self.fb = filebrowser.FileBrowser(self) # объект файл-браузера
        self.fb.show()

    ####### ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ ###################################
    ###################################################################

    # переопределим метод событий mainwindow с целью определения его размеров
    # и регулирования высоты виджета с легендой
    def resizeEvent(self, event):         
        self.wheight = self.size().height()   # определили высоту mainwindow
        
        





        
