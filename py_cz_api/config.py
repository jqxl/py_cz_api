'''Конфиг библиотеки'''

app_name = 'py_cz_api'
app_version = '0.1.2'
app_string = f'Python lib: {app_name} v{app_version}'

'''Количество запросов в секунду не должно превышать 50 от одного участника оборота
товаров. В случае невыполнения данного требования участник оборота товаров может быть
заблокирован.

Использовать в случае асинхронности, т.к.
Среднее время выполнения запросов через requests составляет 1.072 сек
'''
rps = 50
