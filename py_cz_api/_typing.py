from typing import Literal, List

CisStatus = Literal['INTRODUCED', 'WITHDRAWN', 'WRITTEN_OFF', 'EMITTED', 'APPLIED', 'RETIRED', 'DISAGGREGATION', 'DISAGGREGATED', 'APPLIED_NOT_PAID']
'''### Справочник «Статусы КИ»
- `INTRODUCED` - В обороте
- `WITHDRAWN` - Выбыл (только для определенных товарных групп)
- `WRITTEN_OFF` - Списан
- `EMITTED` - Эмитирован
- `APPLIED` - Нанесён
- `RETIRED` - Выбыл (кроме некоторых товарных групп)
- `DISAGGREGATION` - Расформирован (кроме некоторых товарных групп)
- `DISAGGREGATED` - Расформирован (только для определенных товарных групп)
- `APPLIED_NOT_PAID` -Не оплачен (только для определенных товарных групп)
'''

EmissionTypes = List[Literal['LOCAL', 'FOREIGN', 'REMAINS', 'CROSSBORDER', 'REMARK', 'COMMISSION']]
'''### Справочник «Типы эмиссии КИ»
- `LOCAL` - Производство РФ
- `FOREIGN` - Ввезён в РФ
- `REMAINS` - Маркировка остатков
- `CROSSBORDER` - Ввезён из стран ЕАЭС
- `REMARK` - Перемаркировка
- `COMMISSION` - Принят на комиссию от физического лица
'''
