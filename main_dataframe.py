import os
import pandas as pd

import globals

class MainDataframe():
    def __init__(self, mainwindow) -> None:
        self.mainwind = mainwindow

        # предварительно создаём sub_main_df и заполняем её 24-часами времени посекундно
        


        # итерируемся по элементам контейнера (параметрам), генерим для каждого sub_df
        # и добавляем каждый в sub_main_df
        layout = self.mainwind.lay_b_1  # определяем кол-во объектов в контейнере с параметрами
        objs_number = layout.count()    # кол-во объектов (параметров)  
        if objs_number:
            for i in range(objs_number):
                # для каждого параметра из контейнера формируем датафрейм
                sub_df = self.df_formation(i, layout)   # вспомогательный датафрейм
                print(sub_df)
        else:
            print('no objects')


    
    # @brief  Метод, формирующий вспомогательную датафрейм.
    # @detail Метод берёт i-тый параметр из контейнера, определяет архив, к которому принадлежит параметр,
    # выдёргивает из каждого csv-шника именно этот параметр, удаляет дату из 0-й колонки
    # и конкатинирует их все во вспомогательную датафрейм sub_df.
    # @param  i - счётчик для итерации по элементам контейнера с параметрами;
    # @param  layout - контейнер с параметрами;
    # @retval sub_df - датафрейм, состоящая из сконкатинированных столбцов конкретно по заданному параметру.
    def df_formation(self, i, layout):
            param_name = ''
            csv_list = []   # пустой список для имён csv-шников
            # получаем список всех объектов в папке
            item = layout.itemAt(i)                     # получаем i-тый элемент контейнера
            label = item.widget()                       # получаем лейбел
            text = label.text()                         # извлекаем название лейбла
            words_list = text.split(' *')                        # получаем список слов названия
            param_name = words_list[1]                           # имя параметра
            words_list[0] = words_list[0].replace("[", "")       # удаляем скобки из имени архива
            words_list[0] = words_list[0].replace("]", "")
            arch_name = words_list[0]                            # получаем имя архива
            arch_path = globals.arch_dict[arch_name]    # путь к архиву
            objects_list = os.listdir(arch_path)        # список всех объектов в папке
            # составляем список только из csv-шников
            csv_list.clear()    # очищаем список для каждой итерации по элементам контейнера
            for i in range(len(objects_list)):
                if objects_list[i].endswith('csv'):
                    csv_list.append(objects_list[i]) # здесь список csv-шников
            # итерируемся по списку файлов в текущем архиве:
            df = pd.DataFrame({})   # df будет содержать сконкатинированные данные из всех csv-шников по взятому параметру              
            for i in range(len(csv_list)):
                # соединяем путь к архиву с именем файла
                full_path = os.path.join(arch_path, csv_list[i])
                # получаем из csv-файла временный dataframe (tmp_df)
                tmp_df = pd.read_csv(full_path)      # читаем все данные из текущего csv-шника в dataframe
                # извлекаем из tmp_df только нужные колонки (времени и данные параметра)
                col_nms = tmp_df.columns                     # список названий колонок
                tmp_df_2 = tmp_df[[col_nms[1], param_name]]  # извлекли нужные колонки
                col_nms2 = tmp_df_2.columns                  # список названий колонок (для переименования нулевой)
                tmp_df_2 = tmp_df_2.rename(columns={col_nms2[0] : 'time'}) # переименовываем 0-ю колонку
                tmp_df_2 = self.delete_date(tmp_df_2)                   # удаляем дату из колонки
                # конкатинируем с df
                df = pd.concat([df, tmp_df_2])
            # добавляем имя архива к наименованию параметра
            words_list[0] = '[' + words_list[0]
            words_list[0] = words_list[0] + ']'
            col_nms3 = df.columns
            df = df.rename(columns={col_nms3[1] : words_list[0] + ' * ' + col_nms3[1]}) # добавляем к имени параметра название архива
            # сбрасываем индексацию
            df.reset_index(drop=True, inplace=True)
            return df

    # вспомогательный метод, выделяющий из колонки, содержащей дату и время, только время
    def delete_date(self, df):
        col_name = df.columns[0]        # получаем имя 0-й колонки
        tmp_list = []
        for i in range(len(df)):
            tmp = df.loc[i][col_name]
            tmp_list.append(tmp[-8:])   # составляем список только времён
        new_df = df.drop(columns=[col_name])  # удаляем старый столбец
        new_df.insert(0, col_name, tmp_list)  # вставляем новую колонку
        return new_df


        



        