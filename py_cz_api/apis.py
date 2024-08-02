import json
import time
import requests
import asyncio
import aiohttp
import pandas

from . import config
from .classes import Pgs
from .classes import URLStand
from .tokens import Token

class Api:
    def __init__(self,
                 Token: Token,
                 pg: str,
                 product_env: bool = True
                 ):
        '''
        Класс работы с API, содержатся URL запросы из True API CZ
        '''
        self.pg = pg
        self.url_v3, self.url_v4, self.stand = URLStand(product_env).get_urls()
        self.Token = Token
        #self._semaphore = asyncio.Semaphore(50)  # Ограничение на 50 запросов в секунду
        #self._rate_limit_lock = asyncio.Lock()
        self._last_request_time = 0

    @property
    def _url_pg(self) -> str:
        '''Возвращает ?pg="ТГ" для url запроса, где требуется указание pg в запросе'''
        return f'?pg={self.pg}' if self.pg else ''

    def gtin_info(self, gtin_list:list) -> dict:    #TODO q = 1 000 split
        URL = '/product/info'
        url = self.url_v4 + URL
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }
        datas = {'gtins': gtin_list}

        json_string = json.dumps(datas)
        response = requests.post(url, headers=headers, data=json_string)
        data = response.json()
        return data

    def cises_info(self, cis_list: list, pretty: bool = True) -> dict:
        '''Возвращает json ответ от ЧЗ по списку cis
        pretty: False [{'cisInfo':[cis:...]}, {'cisInfo':[cis:...]}]
        pretty: True  [[cis:...]}, [cis:...], [cis:...],]'''

        URL = '/cises/info'
        url = self.url_v3 + URL + self._url_pg
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }

        datas = []
        batch_size = 1000
        delay = 1 / 50  # Ограничение на 50 запросов в секунду

        # Разделение списка cis_list на подсписки по batch_size элементов
        cis_batches = [cis_list[i:i + batch_size] for i in range(0, len(cis_list), batch_size)]

        for batch in cis_batches:
            json_string = json.dumps(batch)
            response = requests.post(url, headers=headers, data=json_string)
            #return response
            data = response.json()
            datas.append(data)
            time.sleep(delay)

        flattened_list = [item for sublist in datas for item in sublist]

        if pretty:
            return [cis['cisInfo'] for cis in flattened_list]
        else:
            return flattened_list

    async def fetch(self, session, url, headers, json_string):
        async with asyncio.Semaphore(50):
            async with asyncio.Lock():
                current_time = time.time()
                elapsed_time = current_time - self._last_request_time
                if elapsed_time < 0.02:
                    await asyncio.sleep(0.02 - elapsed_time)
            self._last_request_time = time.time()
            async with session.post(url, headers=headers, data=json_string) as response:
                return await response.json()

    async def cises_info_aio(self, cis_list: list, pretty: bool = True) -> dict:
        '''Возвращает json ответ от ЧЗ по списку cis
        pretty: False [{'cisInfo':[cis:...]}, {'cisInfo':[cis:...]}]
        pretty: True  [[cis:...]}, [cis:...], [cis:...],]

        :return: json ответ ЧЗ'''

        URL = '/cises/info'
        url = self.url_v3 + URL + self._url_pg
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }

        datas = []
        batch_size = 1000

        # Разделение списка cis_list на подсписки по batch_size элементов
        cis_list_chunks = [cis_list[i:i + batch_size] for i in range(0, len(cis_list), batch_size)]

        total_chunks = len(cis_list_chunks)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for chunk in cis_list_chunks:
                json_string = json.dumps(chunk)
                task = self.fetch(session, url, headers, json_string)
                tasks.append(task)
                #await asyncio.sleep(delay)

            responses = await asyncio.gather(*tasks)
            datas.extend(responses)

        flattened_list = [item for sublist in datas for item in sublist]

        if pretty:
            return [cis['cisInfo'] for cis in flattened_list]
        else:
            return flattened_list


class ApiExtended(Api):
    async def recursive_unpack(self, df:pandas.DataFrame, cis_col:str) -> pandas.DataFrame:
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

        df1 = pandas.DataFrame({cis_col:requestedCiss, 'UNIT':childs})
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

        df1 = pandas.DataFrame({'UNIT':requestedCiss, 'status':requestedCiss_status, 'ownerInn': requestedCiss_ownerInn,'ownerName': requestedCiss_ownerName})
        merge2 = df1.merge(merge, on='UNIT', how='left', suffixes=('_merge', '_df'))
        return merge2
