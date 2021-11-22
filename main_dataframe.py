import os
import pandas as pd

import globals

class MainDataframe():
    def __init__(self, mainwindow) -> None:
        self.mainwind = mainwindow
        param_name = ''
        csv_list = []   # пустой список для имён csv-шников
        # пустая вспомогательная df (будет содержать сконкатинированные данные из всех csv-шников по взятому параметру)
        sub_df = pd.DataFrame({})

        # определяем кол-во объектов в контейнере с параметрами
        layout = self.mainwind.lay_b_1
        objs_number = layout.count()
        if objs_number:
            for i in range(objs_number):
                item = layout.itemAt(i)                     # получаем i-тый элемент контейнера
                label = item.widget()                       # получаем лейбел
                text = label.text()                         # извлекаем название лейбла
                a = text.split(' *')                        # получаем список слов названия
                param_name = a[1]                           # имя параметра
                a[0] = a[0].replace("[", "")                # удаляем скобки из имени архива
                a[0] = a[0].replace("]", "")
                arch_name = a[0]                            # получаем имя архива
                arch_path = globals.arch_dict[arch_name]    # путь к архиву
                objects_list = os.listdir(arch_path)        # список всех объектов в папке
                # составляем список только из csv-шников
                csv_list.clear()    # очищаем список для каждой итерации по элементам контейнера
                for i in range(len(objects_list)):
                    if objects_list[i].endswith('csv'):
                        csv_list.append(objects_list[i]) # здесь список csv-шников

                # итерируемся по списку файлов в текущем архиве:
                for i in range(len(csv_list)):
                    # соединяем путь к архиву с именем файла
                    full_path = os.path.join(arch_path, csv_list[i])

                    # получаем из csv-файла временный dataframe (tmp_df)
                    tmp_df = pd.read_csv(full_path)      # читаем все данные из текущего csv-шника в dataframe

                    # извлекаем из tmp_df только нужные колонки (времени и данные параметра)
                    nm = tmp_df.columns                     # список названий колонок
                    tmp_df_2 = tmp_df[[nm[1], param_name]]  # извлекли нужные колонки
                    nm2 = tmp_df_2.columns                  # список названий колонок (для переименования первой)
                    tmp_df_2 = tmp_df_2.rename(columns={nm2[0] : 'date_time'}) # переименовываем 0-ю колонку

                    # конкатинируем с sub_df
                    sub_df = pd.concat([sub_df, tmp_df_2])

                    # сбрасываем индексацию
                    sub_df.reset_index(drop=True, inplace=True)


                print(sub_df)
                # print(sub_df.head(5))
                
                

                
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
        