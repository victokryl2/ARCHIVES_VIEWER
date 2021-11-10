
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
        wheight = self.size().height()   # определили высоту mainwindow
        maxheight = wheight/3            # задали максимальную высоту виджета относительно mainwindow
        # регулируем высоту виджета 2 согласно количеству графиков
        self.n = 2
        minh = self.n * 20
        if (minh < 30):
            minh = 30
        if (minh > maxheight):
            minh = maxheight
        if (self.n == 2):
            minh = 50    
        self.widget_6.setMinimumHeight(minh)

        
        





        
