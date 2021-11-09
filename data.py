from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd


class Data():
    def __init__(self, filebrowser):
        self.filebrowser = filebrowser

        self.data = pd.DataFrame()          # создаём пустую dataframe
        self.data = self.csv_reading()      # читаем данные из csv в dataframe
        





    def csv_reading(self):
        index = self.filebrowser.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        file_path = self.filebrowser.model.filePath(index)  # получаем по этому индексу путь к объекту
        return pd.read_csv(file_path)
   






        # self.mainwindow = mainwindow
        # self.n = 5                  # кол-во графиков
        # self.m = 10                  # кол-во значений в графиках
        # self.x = []                  # список для оси Х
        # self.y = []                  # список списков значений Y
        # self.graph_names = []             # список легенды (названий графиков)
        # self.vals_list = []             # список для хранения объектов чисел курсора
        # self.colors_list = []        # список цветов rgb

        # # формируем ось Х
        # self.x = list(range(self.m))

        # # формируем список значений Y-ов
        # for i in range(self.n):
        #     self.y = [[random.randint(0, 10) for j in range(self.m)] for i in range(self.n)]

        # # формируем рандомный список объектов чисел курсора
        # for i in range(self.n):
        #     self.vals_list.append(QLabel())
        #     val = random.uniform(-10, 10)
        #     val = round(val, 2)
        #     self.vals_list[i].setNum(val)
        #     self.vals_list[i].setAlignment(Qt.AlignCenter)

        # # формируем рандомный список легенды (названия графиков)
        # for i in range(self.n):
        #     self.graph_names.append(QLabel())
        #     self.graph_names[i].setText('название графика авыпаврпаравпавыпапипмс № ' + str(i))






