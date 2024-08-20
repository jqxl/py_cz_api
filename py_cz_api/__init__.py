'''
Пользовательская ( не официальная )
Библиотека для обращения к True API Честного Знака
Основывается на документации True API Версии 399.0

Для участников системы маркровки продукции с ролями:
Производитель, Импортёр, Оптовая торговля, Розница и иное

Документация True API от Честного знака:
https://markirovka.crpt.ru/ -> Маркровка -> Товарная группа -> Помощь
'''

from .config import app_version as __version__

from .certificates import show_certs
from .classes import Pgs
from .certificates import Certificate
from .tokens import Token
from .apis import Api, ApiDispenser
from .buisness.pd_cz import ApiExtended
