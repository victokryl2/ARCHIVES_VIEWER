import os
import pandas as pd

import globals

class MainDataframe():
    def __init__(self, mainwindow) -> None:
        self.mainwind = mainwindow
        param_name = ''
        csv_list = []   # пустой список для имён csv-шников

        # определяем кол-во объектов в контейнере с параметрами
        layout = self.mainwind.lay_b_1
        objs_number = layout.count()
        if objs_number:
            for i in range(objs_number):
                item = layout.itemAt(i)                     # получаем i-тый элемент контейнера
                label = item.widget()                       # получаем лейбел
                text = label.text()                         # извлекаем название лейбла
                a = text.split(' *')                         # получаем список слов названия
                a[0] = a[0].replace("[", "")                # удаляем скобки из имени архива
                a[0] = a[0].replace("]", "")
                arch_name = a[0]                            # получаем имя архива
                arch_path = globals.arch_dict[arch_name]    # путь к архиву
                objects_list = os.listdir(arch_path)        # список всех объектов в папке
                # составляем список только из csv-шников
                csv_list.clear()    # очищаем список для каждой итерации
                for i in range(len(objects_list)):
                    if objects_list[i].endswith('csv'):
                        csv_list.append(objects_list[i])

                # итерируемся по списку файлов в текущем архиве:
                for i in range(len(csv_list)):
                    # соединяем путь к архиву с именем файла
                    full_path = os.path.join(arch_path, csv_list[i])

                    # получаем из файла временный dataframe (tmp_df)
                    print(full_path)
                    tmp_df = pd.read_csv(full_path)      # читаем данные из csv в dataframe

                    # извлекаем из tmp_df колонки времени и данные параметра
                    # New_D = df[['name','episodes']]


                    # конкатинируем с sub_df
                # print(tmp_df)
                
                

                
        else:
            print('no objects')


    








    # метод, формирующий вспомогательую датафрейм sub_df
    # def sub_df_formation(self, layout):
        # while layout.count():
        #     item = layout.takeAt(0)
        #     widget = item.widget()
        #     if widget is not None:
        #         widget.deleteLater()
        #     else:
        #         self.clearLayout(item.layout())
        