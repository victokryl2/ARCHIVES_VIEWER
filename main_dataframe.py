import os
import pandas as pd

import globals

class MainDataframe():
    def __init__(self, mainwindow) -> None:
        self.mainwind = mainwindow

        # предварительно создаём sub_main_df и заполняем её 24-часами времени посекундно
        l = self.time_list_generate()                   # список "времени" в формате string
        self.sub_main_df = pd.DataFrame({'time': l})    # инициализируем sub_main_df 24-часами времени
    
        # итерируемся по элементам контейнера (параметрам), генерим для каждого sub_df
        # и добавляем каждый в sub_main_df
        layout = self.mainwind.lay_b_1  # определяем кол-во объектов в контейнере с параметрами
        objs_number = layout.count()    # кол-во объектов (параметров)  
        if objs_number:
            for i in range(objs_number):
                # для каждого параметра из контейнера формируем датафрейм
                sub_df = self.df_formation(i, layout)   # вспомогательный датафрейм
                self.add_param_to_sub_main_df(sub_df)
        else:
            print('no objects')

        # globals.main_df = self.cut_sub_main_df(self.sub_main_df)  # удаляем начало и конец DF, не содержащие данных
        globals.main_df = self.sub_main_df
        # print(globals.main_df)

    
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

    # вспомогательный метод, генерящий список времени в формате 00:00:00
    def time_list_generate(self):
        t_tmp = ['00','00','00']
        t = '00:00:00'
        t_list = []
        
        for h in range(24):
            self.hours(t_tmp, h)
            for m in range(60):
                self.minutes(t_tmp, m)
                for s in range(60):
                    self.seconds(t_tmp, t, t_list, s)
        return t_list

    # вспомогательный метод для метода time_list_generate(), генерящий секунды
    def hours(self, t_tmp, h):
        if h < 10:
            t_tmp[0] = '0' + str(h)
        else:
            t_tmp[0] = str(h)
    # вспомогательный метод для метода time_list_generate(), генерящий минуты
    def minutes(self, t_tmp, m):
        if m < 10:
            t_tmp[1] = '0' + str(m)
        else:
            t_tmp[1] = str(m)
    # вспомогательный метод для метода time_list_generate(), генерящий часы
    def seconds(self, t_tmp, t, t_list, s):
        if s < 10:
            t_tmp[2] = '0' + str(s)
        else:
            t_tmp[2] = str(s)
        t = t_tmp[0] + ':' + t_tmp[1] + ':' + t_tmp[2]
        t_list.append(t)




    def add_param_to_sub_main_df(self, df):
        col_list = df.columns           # получаем список имён колонок
        par_n = col_list[1]             # получаем имя параметра
        self.sub_main_df[par_n] = 0     # добавляем к sub_main_df новую нулевую колонку с именем параметра
        # получаем первое значение времени 'time' из df
        time_0_df = df.iloc[0]['time']
        # Ищем индекс такого же значения как time_0_df  в sub_main_df
        indx_tuple = self.sub_main_df.index[self.sub_main_df.time == time_0_df]  # кортеж со списоком индексов искомых значений в столбце
        indx_time_0_df = indx_tuple[0]  # индекс искомого значения
        # получаем длину датафрейм df
        d1_len = len(df)
        # итерируемся по длине d1 и вставляем d1 в sub_main_df
        for i in range(d1_len):
            v = indx_time_0_df + i
            self.sub_main_df.loc[[v], par_n] = df.loc[i][par_n]

    def cut_sub_main_df(self, df):
        # получаем индекс первого ненулевого
        col_names_list = df.columns.tolist()
        col_names_list.pop(0)       # удаляем первый элемент списка (время)
        ind_list = []
        for col in col_names_list:
            tmp_df = df[col]
            ind_list.append(tmp_df.ne(0).idxmax())  # составляем список из индексов первых ненулевых
        first_ind = min(ind_list)
        # получаем индекс последнего ненулевого
        last_ind_list = []
        for col in col_names_list:
            for i in range(len(tmp_df)):
                val = df.loc[i][col]
                if val != 0:
                    ind_list = df.index[df[col] == val].tolist()
                    max_ind = max(ind_list)
            last_ind_list.append(max_ind)
        last_ind = max(last_ind_list)
        # получаем срез строк по первому и последнему индексу
        new_df = df.iloc[first_ind:last_ind+1]
        new_df.reset_index(drop=True, inplace=True)
        return new_df

        



        