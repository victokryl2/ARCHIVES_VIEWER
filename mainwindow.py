
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

        # коннекты УКВ1
        self.pushButton.clicked.connect(self.on_button)

    def on_button(self):
        self.fb = filebrowser.FileBrowser() # объект файл-браузера
        self.fb.show()



        # # создаём экземпляр класса Data
        # self.data = data.Data(self)

        # # создаём экземпляр класса Graphic
        # self.graphic = graphic.Graphic(self)

        # # создаём экземпляр класса Legend
        # self.legend = legend.Legend(self)


    ######## ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ ###################################
    ####################################################################

    # # переопределим метод событий mainwindow с целью определения его размеров
    # # и регулирования высоты виджета с легендой
    # def resizeEvent(self, event):         
    #     wheight = self.size().height()   # определили высоту mainwindow
    #     maxheight = wheight/3            # задали максимальную высоту виджета относительно mainwindow
    #     # регулируем высоту виджета 2 согласно количеству графиков
    #     minh = self.data.n * 20
    #     if (minh < 30):
    #         minh = 30
    #     if (minh > maxheight):
    #         minh = maxheight
    #     if (self.data.n == 2):
    #         minh = 50    
    #     self.widget_2.setMinimumHeight(minh)

        
        





        
