import pandas as pd

from py_cz_api.apis import Api

class ApiExtended(Api):
    '''Расширенный функционал с бизнес логикой под конкретные задачи'''
    async def recursive_unpack(self,
                               df:pd.DataFrame,
                               cis_col:str) -> pd.DataFrame:
        '''Добавляет колоку UNIT в DataFrame, содержащий марки штук продукции из вышестоящих марок

        :param df: - входящий DataFrame
        :param cis_col: - название стобца с марками для распаковки
        :return: DataFrame с новой колонкой UNIT'''
        df[cis_col] = df[cis_col].apply(lambda x: x.replace('(00)', '00', 1) if x.startswith('(00)') else x)
        mark_list = df[cis_col].to_list()

        ans = await self.cises_info_aio(mark_list)

        requestedCiss = []
        childs = []
        requestedCiss_status = []

        for a in ans:
            requestedCiss.append(a['requestedCis'])
            childs.append(a['child'])

        df1 = pd.DataFrame({cis_col:requestedCiss, 'UNIT':childs})
        df2 = df1.explode('UNIT')
        df2['UNIT'] = df2['UNIT'].fillna(df2[cis_col])
        merge = df2.merge(df, on=cis_col, how='left', suffixes=('_merge', '_df'))

        ### TODO рекурсивный метод распаковки до штук, далее опрос о статусе

        mark_list = merge['UNIT'].to_list()
        ans = await self.cises_info_aio(mark_list)

        requestedCiss = []
        childs = []
        requestedCiss_status = []
        requestedCiss_ownerInn = []
        requestedCiss_ownerName = []


        for a in ans:
            requestedCiss.append(a['requestedCis'])
            requestedCiss_status.append(a['status'])
            requestedCiss_ownerInn.append(a['ownerInn'])
            requestedCiss_ownerName.append(a['ownerName'])

        df1 = pd.DataFrame({'UNIT':requestedCiss, 'status':requestedCiss_status, 'ownerInn': requestedCiss_ownerInn,'ownerName': requestedCiss_ownerName})
        merge2 = df1.merge(merge, on='UNIT', how='left', suffixes=('_merge', '_df'))
        return merge2

    def cz_add_cis_info(self,
                        df:pd.DataFrame,
                        cis_col:str,
                        cisInfoCols:list = ['requestedCis',
                                            'status',
                                            'ownerInn',
                                            'producerInn']
                        ) -> pd.DataFrame:
        '''Добавляет в DataFrame столбцы из cises_info'''
        ans = self.cises_info(df['mark_list'].to_list())

        df_ans = pd.json_normalize(ans)[['requestedCis', 'status', 'ownerInn', 'producerInn']]
        merged_df = df.merge(df_ans, left_on='mark_list', right_on='requestedCis', how='left', ).drop(columns=['requestedCis'])
        return merged_df