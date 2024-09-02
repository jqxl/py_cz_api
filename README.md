# Личный проект для автоматизации работы с Честным Знаком через True API

### **<ins>Только для ОС Windows с установленной КриптоПро SCP</ins>**
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-cz-api.svg)](https://pypi.org/project/py-cz-api/)
[![My PyPi bage](https://badge.fury.io/py/py-cz-api.svg)](https://badge.fury.io/py/py-cz-api)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-cz-api)](https://pypi.org/project/py-cz-api)

## Описание

Этот проект предназначен для автоматизации взаимодействия с системой "Честный Знак" через True API. Последняя версия используемого API — 399.0.

Основная цель проекта - упростить процесс получения статусов и владельцев кодов маркировки.

## Подготовка
### Установка КриптоПро SCP
Скачать можно по [ссылке](https://www.cryptopro.ru/downloads)

### Установка зависимостей

Требуется установить вспомогательные библиотеки
```bash
pip install aiohttp, pywin32, PyJWT
```

### Установка библиотеки
Установть `py_cz_api` можно с помощью менеджера пакетов [pip](https://pypi.org/project/py-cz-api/)
```bash
pip install py-cz-api
```

### Инициализация классов и опрос ЧЗ о статусе марок:

```python
import py_cz_api

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.Api(token, py_cz_api.Pgs.ncp)

# Список марок для запроса
mark_list = ['01230000157926=Mflh=dAAAA']

# Выполнение запроса
ans = api.cises_info(mark_list)

# Печать dict ответа от API
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
- `Certificate` - ЭЦП для шифрования данных __исключено для корректной работы PyPi__
- `Token` - авторизационный токен ЧЗ
- `Api` - отправка запросов в ЧЗ
- `ApiDispenser` - формирование и скачивание Документов выгрузки
- `ApiExtended` - добавление стобцам pandas.DataFrame данные от `Api`

## Реализованный список эндпоинтов:

### class: `Api`
- `/cises/short/list`
- `/cises/info`
- `/cises/history`
- `/product/info`
- `/doc/{documentId}/info`
- `/doc/cises`
### class: `ApiDispenser`
- `/dispenser/tasks`
- `/dispenser/tasks/{taskId}`
- `/dispenser/results/{taskId}`
- `/dispenser/results/{taskId}/file`

## Дополнительная информация

Для получения дополнительной информации и документации по использованию True API, пожалуйста, обратитесь к официальной документации True API версии 418.0.
