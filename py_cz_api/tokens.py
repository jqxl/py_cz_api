import json
import requests

from datetime import datetime, timedelta
from jwt import decode as jwt_decode

from .certificates import Certificate
from .exceptions import TokenExpiredError


class Token:
    '''Интерфейс класса токен
    Реализуй свои методы если хочешь получать токен
    другими способами, отличные от работы с ЭЦП

    Можно вытягивать токен из учётной системы типа 1С, SAP
    через любые протоколы передачи данных

    :param: `value` - само значение токена'''

    value: str
    jwt: json
    jwt_exp: timedelta

    def __init__(self, value:str):
        self.value: str = value
        self.jwt: json
        self.jwt_exp: timedelta

        self.token_validate()

    def token_validate(self):
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
        '''Получить токен по сертфикату'''
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
    def create_from_http(url:str) -> 'Token':
        raise NotImplementedError
