import pandas as pd

from py_cz_api.apis import Api

class ApiExtended(Api):
    '''Расширенный функционал с бизнес логикой под конкретные задачи'''
    def df_unpack(self,
                 df:pd.DataFrame,
                 cis_col:str,
                 needs_explode:bool = True,
                 fillna:bool = True) -> pd.DataFrame:
        '''Добавляет колоку UNIT в DataFrame, содержащий марки штук продукции из вышестоящих марок

        :param df: - входящий DataFrame
        :param cis_col: - название стобца с марками для распаковки
        :return: DataFrame с новой колонкой UNIT'''
        ### TODO рекурсивный метод распаковки до штук
        merge = self.df_add_cis_info(df, cis_col, cisInfoCols=['child'])
        if needs_explode: merge = merge.explode('child')
        if fillna: merge['child'] = merge['child'].fillna(merge[cis_col])
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
        merge = df.merge(df_ans, left_on=cis_col, right_on=join_col, how='left').drop(columns=[join_col])
        return merge

    def _doc_id_from_cis(self,
                         cis:str) -> str:
        '''
        ## Получить послений doc_id УПД по маркировке
        '''
        ans = self.cises_history(cis)
        df = pd.DataFrame(ans)
        df = df[df['docId'].str.startswith('ON_NSCHFDOPPRMARK_2BM')]
        df.sort_values(by='operationDate', inplace=True)
        return df['docId'].iloc[0]

    def df_add_cis_short_info(self,
                        df:pd.DataFrame,
                        cis_col:str,
                        cisInfoCols:list = ['status',
                                            'ownerInn',
                                            'receiptDate']
                        ) -> pd.DataFrame:
        '''Добавляет в DataFrame столбцы из cisInfoCols'''
        join_col = 'requestedCis'
        cisInfoCols.append(join_col)
        ans = self.cises_short_list(df[cis_col].to_list())
        df_ans = pd.json_normalize(ans)[cisInfoCols]
        merge = df.merge(df_ans, left_on=cis_col, right_on=join_col, how='left').drop(columns=[join_col])
        return merge
