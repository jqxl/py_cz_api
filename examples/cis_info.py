import py_cz_api

# Вариант с созданием трёх объектов: Сертификат, Токен, API
# from py_cz_api import Token, Api, Certificate
# from py_cz_api import Pgs
# certificate = Certificate('02a3eec200e0b02b874d7e0ca9d5d53bd7')     # записываем сертификат в переменную
# token = Token.create_from_cert(certificate)                         # получаем Token авторизации
# api = Api(Token=token, pg=Pgs.ncp)                                  # передаём в API авторизационный токен

# Ускоренное создание API
api = py_cz_api.create_api_cert(
    serialnumber='02a3eec200e0b02b874d7e0ca9d5d53bd7',
    pg=py_cz_api.Pgs.ncp
)

# Список марок для запроса
mark_list = ['01230000157926=Mflh=dAAAA']

# Выполнение запроса
ans = api.cises_info(mark_list)

# Печать dict ответа от API
print(ans)