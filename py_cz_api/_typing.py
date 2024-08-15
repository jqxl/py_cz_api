# TODO частично покрыть тайпингом
from typing import Literal, List

CisStatus = Literal[
    'INTRODUCED',  # В обороте
    'WITHDRAWN',  # Выбыл (только для определенных товарных групп)
    'WRITTEN_OFF',  # Списан
    'EMITTED',  # Эмитирован
    'APPLIED',  # Нанесён
    'RETIRED',  # Выбыл (кроме некоторых товарных групп)
    'DISAGGREGATION',  # Расформирован (кроме некоторых товарных групп)
    'DISAGGREGATED',  # Расформирован (только для определенных товарных групп)
    'APPLIED_NOT_PAID'  # Не оплачен (только для определенных товарных групп)
]
EmissionTypes = List[Literal['LOCAL', 'FOREIGN', 'REMAINS', 'CROSSBORDER', 'REMARK', 'COMMISSION']]
