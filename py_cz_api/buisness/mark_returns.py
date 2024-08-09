import pandas as pd

from .pd_cz import ApiExtended

needs_cols = ['status',
              'ownerInn',
              'child',
              'producerInn']

class Returns:
    '''
    ## Помощник возвратов
    Передаёшь список возвращаемых марок, получаешь готовые списки маркировки для формирования УКД для каждой реализации

    Механизм:
    - Проверка статусов и владельцев кодов маркировки
      - [ ] Формируется .txt файл на Отказ возрата по причине нарушения оборота маркируемой продукции
    - Узнаются оригинальные УПД
      - [ ] К каждому коду маркировки присвается оригинальный документ УПД
      - [ ] Из документа УПД убираются возвращаемые коды маркировки, попутно разформируются упаковки, если возвращаются штуки
    - Подготавливаются файлы пользователю
      - [ ] Формируется список КМ для загрузки в документ 1С: Корректировка Реализации
    - Отправка файлов пользователю
      - [ ] Отправляется отказ возврата
      - [ ] Отправляется Excel таблица с марками для 1С
    '''
    whom_inn:str
    us_inn:str
    input_mark_list:list
    input_mark_df:pd.DataFrame

    taboo_mark_list:list

    def __init__(self,
                 mark_list:list,
                 whom_inn:str,
                 us_inn:str):
        self.input_mark_list = mark_list
        self.input_mark_df = pd.DataFrame({'input_mark_list':mark_list})
        self.whom_inn = whom_inn
        self.us_inn = us_inn

    def foo():
        pass
