def character_escaping_url(cis: str):
    escape_table = {'!': '%21', '\\': '%5C', '"': '%22', '%': '%25',
                    '&': '%26', "'": '%27', '*': '%2A', '+': '%2B',
                    '-': '%2D', '.': '%2E', '/': '%2F', '_': '%5F',
                    ',': '%2C', ':': '%3A', ';': '%3B', '=': '%3D',
                    '<': '%3C', '>': '%3E', '?': '%3F', '(': '%28',
                    ')': '%29'}
    return ''.join(escape_table.get(char, char) for char in cis)

def link_cis_list(cis_list: list):
    '''Делает ссылку на марку в кабинете, экранруя символы'''
    return ['https://tobacco.crpt.ru/cis/' + character_escaping_url(cis) for cis in cis_list]


def check_dig_ean_13(code: str) -> int:
    '''Вывод контрольной суммы при генерации EAN-13 кода
    Возвращает контрольную сумму'''
    if len(code) != 12 or not code.isdigit():
        return None
    evensum = sum(int(code[i]) for i in range(1, 12, 2))
    oddsum = sum(int(code[i]) for i in range(0, 12, 2))
    total = evensum * 3 + oddsum
    checksum = (10 - (total % 10)) % 10
    return checksum