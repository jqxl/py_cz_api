'''Модуль работы с Токеном авторазиации ЧЗ для доступа к API'''
import json
import requests

from typing import Dict, Any

from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from jwt import decode as jwt_decode

from .certificates import Certificate
from .exceptions import TokenExpiredError


class Token:
    '''Класс Токен - хранит в себе сам Токен и позволяет проверить его актуальность и расшифровать содержимое\n
Можно вытягивать токен из учётной системы типа 1С, SAP через любые протоколы передачи данных'''
    value: str
    jwt: Dict[str, Any]
    jwt_exp: timedelta

    def __init__(self, value:str):
        '''### Чтобы создать класс `Token`, передай ему любым доступным способом значение Токена авторизации
#### Либо получи его с помощью конструкторов:
- `create_from_cert` с помощью ЭП и указания Серийного номера ЭП
- `create_from_http` с помощью get запроса к учетной системе и базовой авторизации логином и паролем

:param value: само значение токена'''
        self.value: str = value
        self.token_validate()

    def token_validate(self) -> None:
        '''Проверка жизни токена

:raises TokenExpiredError: Если токен устарен'''
        if self.time_left.total_seconds() < 0:
            raise TokenExpiredError('JWT токен устарел, требуется перевыпустить токен')

    @property
    def jwt(self) -> json:
        decoded = jwt_decode(jwt=self.value, options={'verify_signature': False})
        return decoded

    @property
    def jwt_exp(self) -> timedelta:
        return datetime.fromtimestamp(self.jwt['exp'])

    @property
    def time_left(self) -> timedelta:
        return self.jwt_exp - datetime.now()

    def __repr__(self) -> str:
        return f'TimeLeft: {self.time_left}'

    def __str__(self) -> str:
        return Token.value

    @staticmethod
    def create_from_cert(Certificate: Certificate) -> 'Token':
        '''Получить токен по сертфикату ЭП

:param Certificate: Экземпляр класса, работающий с ЭП

:return Token: Инициализированный класс `Token`'''

        url = 'https://markirovka.crpt.ru/api/v3/true-api/auth/key'
        headers = {'accept': 'application/json'}

        resp_json = requests.get(url, headers=headers).json()
        uuid, data = resp_json['uuid'], resp_json['data']

        sSignedData = Certificate.sign_data(data, 'ascii')

        url = 'https://markirovka.crpt.ru/api/v3/true-api/auth/simpleSignIn'
        headers = {'accept': 'application/json',
                   'Content-Type': 'application/json'}
        send = {'uuid': uuid,
                'data': sSignedData}

        response = requests.post(url, headers=headers, data=json.dumps(send))

        token = response.json()['token']

        return Token(token)

    @staticmethod
    def create_from_http(url:str, username:str, password:str) -> 'Token':
        '''Отпавряет на указанный `URL` http get запрос на получение Token'а из учётной системы по типу 1C / SAP / Мой Склад\n
По необходимости, перепишите функцию отправки и обработки полученного ответа самостоятельно\n
*! Предварительно нужно настроить отдачу токена по `URL` в Вашей учётной системе !*

:return Token: Инициализированный класс `Token`'''
        auth = HTTPBasicAuth(username.encode('utf-8'), password.encode('utf-8'))
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            token = Token(response.text)
            token.token_validate()
            return token
        else:
            raise ConnectionError(response, response.text)
