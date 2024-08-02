'''
Пользовательская ( не официальная )
Библиотека для обращения к True API Честного Знака
Основывается на документации True API Версии 399.0

Для участников системы маркровки продукции с ролями:
Производитель, Импортёр, Оптовая торговля, Розница и иное

Документация True API от Честного знака:
https://markirovka.crpt.ru/ -> Маркровка -> Товарная группа -> Помощь
'''

from .certificates import show_certs
from .classes import Pgs
from .certificates import Certificate
from .tokens import Token
from .apis import Api
from .apis import ApiExtended

def create_api_cert(serialnumber: str,
               pg: Pgs,
               product_env: bool = True) -> Api:
    '''
    Возвращает класс API для взаимодействия с ЧЗ\n
    Посмотреть ЭП: `py_cz_api.show_cert()`\n
    :param str serialnumbe: - Серийный номер ЭП
    :param Pgs pg: - Основная товарная группа, прим: `Pgs.tabacco`
    :param bool product_env: - Продуктовый контур
    '''
    certificate = Certificate(serialnumber)
    token = Token.create_from_cert(certificate)
    api = Api(Token=token,pg=pg, product_env=product_env)
    return api
