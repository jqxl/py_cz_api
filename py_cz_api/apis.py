import json
import time
import requests
import asyncio
import aiohttp

from ._typing import CisStatus, EmissionTypes
from ._typing import Pgs, URLStand, CisInfo

from .tokens import Token
from typing import List, Optional

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
        self._last_request_time = 0

    def gtin_info(self, gtin_list:list) -> dict:    #TODO q = 1 000 split
        '''### 5.5.1. Метод получения информации о товаре по GTIN товара
В результате успешного выполнения запроса по списку кодов товаров в ответе возвращается
массив с информацией о товарах по запрошенным КИ. В результирующем * .json также может
содержаться набор полей, специфичных для товара конкретной товарной группы (см.
«Справочник "Дополнительные параметры в ответе в зависимости от товарных групп"»).
Действует следующее ограничение: не более 1000 значений «gtin» («Код товара») в параметре
«gtins» («Массив кодов товаров»).
В ответе метода возвращается информация только по карточкам товаров, для которых значения
441
признаков «goodTurnFlag» («Признак готовности товара к обороту») и «goodMarkFlag»
(«Признак готовности к маркировке») равны «true».

:param gtin_list: список GTIN'ов'''
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

    def cises_info(self, cis_list: list, pretty: bool = True) -> List[CisInfo]: # TODO type-hinting CisInfo and pydentic validation
        '''### 5.1.2. Метод получения общедоступной информации о КИ по списку
Метод возвращает подробную информацию о запрашиваемом списке КИ / КиЗ: в одном запросе
указывается как один КИ / КиЗ, так и несколько КИ / КиЗ (не более 1000)

:param pretty: True возвращает словарь типа `[{},{},{}]` без `['cisInfo':{}, 'cisInfo':{}, 'cisInfo':{}]`'''

        URL = '/cises/info'
        pg = self.pg
        url = self.url_v3 + URL + f'?{pg=}'
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
            return [cis['cisInfo'] for cis in flattened_list if 'cisInfo' in cis and cis['cisInfo']]
            #return [cis['cisInfo'] for cis in flattened_list]
        else:
            return flattened_list

    async def _fetch(self, session, url, headers, json_string):
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
        '''### 5.1.2. Метод получения общедоступной информации о КИ по списку
Метод возвращает подробную информацию о запрашиваемом списке КИ / КиЗ: в одном запросе
указывается как один КИ / КиЗ, так и несколько КИ / КиЗ (не более 1000)

:param cis_list: Список Кодов Маркировки
:param pretty: True возвращает словарь типа `[{},{},{}]` без `['cisInfo':{}, 'cisInfo':{}, 'cisInfo':{}]`'''

        URL = '/cises/info'
        pg = self.pg
        url = self.url_v3 + URL + f'?{pg}'
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }

        datas = []
        batch_size = 1000

        cis_list_chunks = [cis_list[i:i + batch_size] for i in range(0, len(cis_list), batch_size)]

        async with aiohttp.ClientSession() as session:
            tasks = []
            for chunk in cis_list_chunks:
                json_string = json.dumps(chunk)
                task = self._fetch(session, url, headers, json_string)
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            datas.extend(responses)

        flattened_list = [item for sublist in datas for item in sublist]

        if pretty:
            return [cis['cisInfo'] for cis in flattened_list if 'cisInfo' in cis and cis['cisInfo']]
        else:
            return flattened_list

    def cises_history(self, cis:str) -> dict:
        '''### 5.2. Метод получения истории движения КИ
Метод возвращает информацию о движении (истории) запрашиваемых КИ (в одном запросе
указывается один КИ) по событиям, в которых участник оборота товаров принимал участие, чей
токен используется при выполнении запроса.

Каждому участнику оборота товаров доступна информация о производителе продукции,
продавце и текущем владельце. Если КИ выведен из оборота, то информация о текущем
владельце не возвращается.

:param cis: Код Маркировки'''
        URL = '/cises/history'
        url = self.url_v3 + URL + f'?{cis=}'
        headers = {
            'accept': '*/*',
            "Authorization": 'Bearer ' + self.Token.value
        }
        response = requests.post(url, headers=headers)
        data = response.json()
        return data

    def doc_info(self,
                 documentId:str,
                 *,
                 body: bool = False,
                 content: bool = False,
                 limit: int = 36_000
                 ) -> dict:
        '''### 6.4. Метод получения содержимого документа по идентификатору

:param documentId: ID документа, формируемый в ГИС МТ, или ИдФайл для УД
:param body: Признак необходимости в теле ответа содержимого документа
:param content: Признак необходимости контента документа в теле ответа
:param limit: Количество кодов в теле документе
        '''
        _body = f'&{body=}'.lower()
        _content = f'&{content=}'.lower()
        _limit = f'&{limit=}'.lower()
        URL = f'/doc/{documentId}/info'
        pg = self.pg
        url = self.url_v4 + URL + f'?{pg=}' + _body + _content
        headers = {
            'accept': '*/*',
            "Authorization": 'Bearer ' + self.Token.value
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data

    def doc_cises(self,
                  documentId:str) -> dict:
        '''### Метод получения списка кодов идентификации и кодов товара по идентификатору документа
Метод используется для получения списка КИ и кодов товара по ID документа, обработанного
успешно или обработанного с ошибкой. В запросе может быть указан только один ID документа.
Метод не предназначен для запроса информации по УПД и УКД. Метод возвращает до 30000 КИ
(ограничение для документов прямой подачи 30000 КИ в одном документе), верхний уровень
агрегатов не возвращается.

:param documentId: ID документа, формируемый в ГИС МТ, или ИдФайл для УД
        '''
        URL = f'/doc/cises'
        productGroup = self.pg
        url = self.url_v3 + URL + f'?{documentId=}' + f'&{productGroup=}'
        headers = {
            'accept': '*/*',
            "Authorization": 'Bearer ' + self.Token.value
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data

    def cises_short_list(self,
                         mark_list:list,
                         pretty:bool=True) -> dict:
        '''### Метод получения общедоступной информации о КИ по списку (упрощённый атрибутивный состав)
Метод предназначен для отгрузки / приёмки товара всех товарных групп, используя информацию только из «cis» («Массив КИ»).

*Из аналитического: есть `receiptDate` - дата вывода из оборота и `approvementDocument` номера разрешительной документации*

:param mark_list: Список Кодов Маркировки
:param pretty: True возвращает словарь типа `[{},{},{}]` без `['result':{}, 'result':{}, 'result':{}]`'''
        URL = '/cises/short/list'
        url = self.url_v3 + URL
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }

        datas = []
        batch_size = 1000

        cis_batches = [mark_list[i:i + batch_size] for i in range(0, len(mark_list), batch_size)]

        for batch in cis_batches:
            json_string = json.dumps(batch)
            response = requests.post(url, headers=headers, data=json_string)
            data = response.json()
            datas.append(data)

        flattened_list = [item for sublist in datas for item in sublist]

        if pretty:
            return [cis['result'] for cis in flattened_list if 'result' in cis and cis['result']]
        else:
            return flattened_list

    async def cises_short_list_aio(self, cis_list: list, pretty: bool = True) -> dict:
        '''### Метод получения общедоступной информации о КИ по списку (упрощённый атрибутивный состав)
Метод предназначен для отгрузки / приёмки товара всех товарных групп, используя информацию только из «cis» («Массив КИ»).

*Из аналитического: есть `receiptDate` - дата вывода из оборота и `approvementDocument` номера разрешительной документации*

:param mark_list: Список Кодов Маркировки
:param pretty: True возвращает словарь типа `[{},{},{}]` без `['result':{}, 'result':{}, 'result':{}]`'''
        URL = '/cises/short/list'
        url = self.url_v3 + URL
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.Token.value
        }

        datas = []
        batch_size = 1000

        cis_list_chunks = [cis_list[i:i + batch_size] for i in range(0, len(cis_list), batch_size)]

        async with aiohttp.ClientSession() as session:
            tasks = []
            for chunk in cis_list_chunks:
                json_string = json.dumps(chunk)
                task = self._fetch(session, url, headers, json_string)
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            datas.extend(responses)

        flattened_list = [item for sublist in datas for item in sublist]

        if pretty:
            return [cis['result'] for cis in flattened_list if 'result' in cis and cis['result']]
        else:
            return flattened_list

class ApiDispenser:
    '''### Методы формирования выгрузок данных из ГИС МТ
Максимальное количество созданных заданий на выгрузку для одной товарной группы составляет 10 раз в день\n
При достижении указанного ограничения создание заданий на выгрузку станет доступно на следующие сутки
    '''
    inn:str
    token:Token
    pg:str

    taskId:str
    doc_name:str

    def __init__(self,
                 token:Token,
                 pg:str,
                 product_env:bool=True,
                 *,
                 inn:str
                 ) -> None:
        self.inn = inn
        self.token = token
        self.pg = pg
        self.url_v3, self.url_v4, self.stand = URLStand(product_env).get_urls()


    def create_task_FILTERED_CIS_REPORT(self,
                                        status:CisStatus,
                                        product_group_code:int,
                                        gtins:list,
                                        emissionTypes:EmissionTypes,
                                        ) -> str:
        '''### 8.1.3. Получение списка КИ участника оборота товаров по заданному фильтру

Выгрузка предназначена для получения сведений о КИ, находящихся на балансе у участника
оборота товаров. У участника оборота товаров, запрашивающего данные из ГИС МТ должен
быть подписан договор по товарной группе, указанной в параметре «productGroupCode»
(«Товарная группа»).

Вывод сведений о КИ осуществляется с учётом установленных фильтров в параметре «params»
(«Строка параметров задания на выгрузку в формате * .json»).

:param status: Статус КМ
:param product_group_code: Циферное представление Товарной Группы. прим: `16` для `НСП`
:param gtins: Список GTIN'ов
:param emissionTypes: Тип эмиссии Кода Маркировки
        '''
        URL = '/dispenser/tasks'
        url = self.url_v3 + URL

        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            "Authorization": 'Bearer ' + self.token.value
        }

        body = json.dumps({
            "format": "CSV",
            "name": "FILTERED_CIS_REPORT",
            "periodicity": "SINGLE",
            "productGroupCode": str(product_group_code),
            "params": json.dumps({
                "participantInn": self.inn,
                "packageType": ["UNIT", "LEVEL1"],
                "status": status,
                "includeGtin": gtins,
                "emissionTypes": emissionTypes,
                "turnoverTypes": ["SELLING"]
            })
        })

        response = requests.post(url, headers=headers, data=body)
        data = response.json()
        self.taskId = data['id']
        self.doc_name = data['name']
        return response.json()

    def status_check(self,
                     taskId:Optional[str],
                     product_group_code:int) -> dict:
        '''### 8.2. Метод получения статуса задания на выгрузку
Метод предназначен для получения статуса задания на выгрузку по идентификатору задания, полученному в ответе метода «Метод создания нового задания на выгрузку»

:param taskId: ID задания
:param product_group_code: Циферное представление Товарной Группы. прим: `16` для `НСП`'''
        if taskId:
            self.taskId = taskId
        URL = f'/dispenser/tasks/{taskId}?pg=' + str(product_group_code)
        url = self.url_v3 + URL

        headers = {
            "Authorization": 'Bearer ' + self.token.value
        }
        response = requests.get(url, headers=headers)
        return response

    def results_check(self,
                     taskId:Optional[str],
                     product_group_code:int) -> dict:
        '''
        ### 8.4. Метод получения результирующих ID выгрузок данных
Данный метод позволяет получить список результирующих идентификаторов выгрузок для скачивания сформированных файлов с данными.

:param taskId: ID задания
:param product_group_code: Циферное представление Товарной Группы. прим: `16` для `НСП`'''
        if taskId:
            self.taskId = taskId
        URL = f'/dispenser/results/{taskId}?page=0?size=10?pg={str(product_group_code)}?task_ids=["{taskId}"]'
        url = self.url_v3 + URL

        headers = {
            "Authorization": 'Bearer ' + self.token.value
        }
        response = requests.get(url, headers=headers)
        return response

    def tesults_zip(self,
                    taskId:Optional[str],
                    product_group_code:int) -> dict:
        '''### 8.5. Метод получения ZIP-файла выгрузки
Метод предоставляет возможность скачивания выгрузки в статусе «COMPLETED» («Выполнено») по идентификатору выгрузки, полученному в ответе метода «Метод получения
результирующих ID выгрузок данных».

:param taskId: ID задания
:param product_group_code: Циферное представление Товарной Группы. прим: `16` для `НСП`'''
        if taskId:
            self.taskId = taskId
        URL = f'/dispenser/results/{taskId}/file?pg=' + str(product_group_code)
        url = self.url_v3 + URL

        headers = {
            'accept': '*/*',
            "Authorization": 'Bearer ' + self.token.value
        }
        response = requests.get(url, headers=headers)
        return response
