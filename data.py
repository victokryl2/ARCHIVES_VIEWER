from PyQt5.QtWidgets import *
import pandas as pd


class Data():
    def __init__(self, filebrowser):
        self.filebrowser = filebrowser

        self.data = pd.DataFrame()          # создаём пустую dataframe      

        # self.data = self.csv_reading()      # читаем данные из csv в dataframe


    def csv_reading(self):
        index = self.filebrowser.treeView.currentIndex()    # получаем индекс объекта, с которым производить действие
        file_path = self.filebrowser.model.filePath(index)  # получаем по этому индексу путь к объекту
        return pd.read_csv(file_path)
   