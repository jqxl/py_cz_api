import pandas as pd

from .pd_cz import ApiExtended

needs_cols = ['status',
              'ownerInn',
              'child',
              'producerInn']

class Returns:
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
