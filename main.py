import sys
from PyQt5 import QtWidgets

import mainwindow

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = mainwindow.MainWindow()        # Создаём объект класса ExampleApp
    window.show()                           # показываем окно
    app.exec_()                             # запускаем приложение
    

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()