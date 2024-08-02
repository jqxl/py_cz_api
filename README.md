# Личный проект для автоматизации работы с Честным Знаком через True API

## Описание

Этот проект предназначен для автоматизации взаимодействия с системой "Честный Знак" через True API. Последняя версия используемого API — 399.0.

Основная цель проекта - упростить процесс получения статусов и владельцев кодов маркировки.

## Использование
### Подготовка

Требуется установить вспомогательные библиотеки
```bash
pip install aiohttp, pywin32, PyJWT
```

### Установка
Установить `py_cz_api` можно с помощью `pip` и ссылки:
```bash
pip install git+https://github.com/jqxl/py_cz_api.git
```

### Инициализация класса и опрос ЧЗ о статусе марок:
Авторизационный токен получается через электронную подпись, в `create_api_cert` передаётся серийный номер ЭП
*Только для ОС Windows*
```python
import py_cz_api
api = py_cz_api.create_api_cert(
    serialnumber='02a3eec200e0b02b874d7e0ca9d5d53bd7',
    pg=py_cz_api.Pgs.ncp)
mark_list = ['01230000157926=Mflh=dAAAA']
ans = api.cises_info(mark_list)
print(ans)
```

### Просмотр сертификатов в личном хранилище:
Посмотреть список сертификатов в хранилище
*Только для ОС Windows*
```python
import py_cz_api
py_cz_api.show_certs()
```

## Классы
Каждый элемент автономен и допускает свою реализацию через наследование
- `Certificate` - ЭЦП для шифрования данных
- `Token` - авторизационный токен ЧЗ
- `Api` - отправка запросов в ЧЗ

## Реализованный список эндпоинтов:

- `/cises/info` - синхронный и асинхронный
- `/product/info` - синхронный

## Дополнительная информация

Для получения дополнительной информации и документации по использованию True API, пожалуйста, обратитесь к официальной документации True API версии 399.0.
