import asyncio

from py_cz_api import Token, Api, Certificate
from py_cz_api import Pgs

def main():
    certificate = Certificate('02a3eec200e0b02b874d7e0ca9d5d53bd7')     # записываем сертификат в переменную
    token = Token.create_from_cert(certificate)                         # получаем Token авторизации
    api = Api(Token=token, pg=Pgs.ncp)                                  # передаём в API авторизационный токен

    # Список марок для запроса
    mark_list = ['01230000157926=Mflh=dAAAA']

    # Выполнение запроса
    ans = api.cises_info_aio(mark_list)
    return ans

if __name__ == '__main__':
    ans = asyncio.run(main())
    print(ans)