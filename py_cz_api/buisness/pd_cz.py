import pandas as pd

from py_cz_api.apis import Api

class ApiExtended(Api):
    '''Расширенный функционал с бизнес логикой под конкретные задачи'''
    def df_unpack(self,
                 df:pd.DataFrame,
                 cis_col:str,
                 needs_explode:bool = True) -> pd.DataFrame:
        '''Добавляет колоку UNIT в DataFrame, содержащий марки штук продукции из вышестоящих марок

        :param df: - входящий DataFrame
        :param cis_col: - название стобца с марками для распаковки
        :return: DataFrame с новой колонкой UNIT'''
        ### TODO рекурсивный метод распаковки до штук
        ans = self.cises_info(df[cis_col].to_list())
        df_ans = pd.json_normalize(ans)[['requestedCis', 'child']]
        merge = df.merge(df_ans, left_on=cis_col, right_on='requestedCis', how='left').drop(columns=['requestedCis'])
        if needs_explode: merge = merge.explode('child')
        return merge

    def df_add_cis_info(self,
                        df:pd.DataFrame,
                        cis_col:str,
                        cisInfoCols:list = ['status',
                                            'ownerInn']
                        ) -> pd.DataFrame:
        '''Добавляет в DataFrame столбцы из cisInfoCols'''
        join_col = 'requestedCis'
        cisInfoCols.append(join_col)

        ans = self.cises_info(df[cis_col].to_list())

        df_ans = pd.json_normalize(ans)[cisInfoCols]
        merged_df = df.merge(df_ans, left_on='mark_list', right_on=join_col, how='left', ).drop(columns=[join_col])
        return merged_df