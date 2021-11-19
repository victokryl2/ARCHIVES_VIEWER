import globals

class MainDataframe():
    def __init__(self, mainwindow) -> None:
        self.mainwind = mainwindow

        # определяем кол-во объектов в контейнере с параметрами
        layout = self.mainwind.lay_b_1
        obj_number = layout.count()
        print(obj_number)
        if obj_number:
            for i in range(obj_number):
                item = layout.itemAt(i) # получаем i-тый элемент контейнера
                label = item.widget()   # получаем лейбел
                text = label.text()     # извлекаем название лейбла
                a = text.split(' ')     # получаем список слов названия
                a[0] = a[0].replace("[", "")   # удаляем скобки из имени архива
                a[0] = a[0].replace("]", "")
                arch_name = a[0]        # получаем имя архива
                arch_path = globals.arch_dict[arch_name]
                print(arch_path)
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
        