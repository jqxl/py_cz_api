from enum import Enum

class mark_list(list):
    pass

class Pgs(str, Enum):
    '''
    Enum representing supported product groups.\n
    ```python
    pg: str = Pgs.ncp
    ```

    - 1  `lp` - Предметы одежды, бельё постельное, столовое, туалетное и кухонное\n
    - 2  `shoes` - Обувные товары\n
    - 3  `tobacco` - Табачная продукция\n
    - 4  `perfumery` - Духи и туалетная вода\n
    - 5  `tires` - Шины и покрышки пневматические резиновые новые\n
    - 6  `electronics` - Фотокамеры (кроме кинокамер), фотовспышки и лампы-вспышки\n
    - 8  `milk` - Молочная продукция\n
    - 9  `bicycle` - Велосипеды и велосипедные рамы\n
    - 10 `wheelchairs` - Медицинские изделия\n
    - 12 `otp` - Альтернативная табачная продукция\n
    - 13 `water` - Упакованная вода\n
    - 14 `furs` - Товары из натурального меха\n
    - 15 `beer` - Пиво, напитки, изготавливаемые на основе пива, слабоалкогольные напитки\n
    - 16 `ncp` - Никотиносодержащая продукция\n
    - 17 `bio` - Биологически активные добавки к пище\n
    - 19 `antiseptic` - Антисептики и дезинфицирующие средства\n
    - 20 `petfood` - Корма для животных\n
    - 21 `seafood` - Морепродукты\n
    - 22 `nabeer` - Безалкогольное пиво\n
    - 23 `softdrinks` - Соковая продукция и безалкогольные напитки\n
    - 26 `vetpharma` - Ветеринарные препараты\n
    - 27 `toys` - Игры и игрушки для детей\n
    - 28 `radio` - Радиоэлектронная продукция\n
    - 31 `titan` - Титановая металлопродукция\n
    - 32 `conserve` - Консервированная продукция\n
    - 33 `vegetableoil` - Растительные масла\n
    - 34 `opticfiber` - Оптоволокно и оптоволоконная продукция\n
    - 35 `chemistry` - Парфюмерные и косметические средства и бытовая химия\n
    - 36 `books` - Печатная продукция\n
    - 38 `pharmaraw` - Фармацевтическое сырьё, лекарственные средства\n
    - 39 `construction` - Строительные материалы
    '''

    lp = "lp"
    shoes = "shoes"
    tobacco = "tobacco"
    perfumery = "perfumery"
    tires = "tires"
    electronics = "electronics"
    milk = "milk"
    bicycle = "bicycle"
    wheelchairs = "wheelchairs"
    otp = "otp"
    water = "water"
    furs = "furs"
    beer = "beer"
    ncp = "ncp"
    bio = "bio"
    antiseptic = "antiseptic"
    petfood = "petfood"
    seafood = "seafood"
    nabeer = "nabeer"
    softdrinks = "softdrinks"
    vetpharma = "vetpharma"
    toys = "toys"
    radio = "radio"
    titan = "titan"
    conserve = "conserve"
    vegetableoil = "vegetableoil"
    opticfiber = "opticfiber"
    chemistry = "chemistry"
    books = "books"
    pharmaraw = "pharmaraw"
    construction = "construction"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.name


class URLStand:
    def __init__(self, product:bool = True):
        """stand: str = 'product' or 'demo'"""
        self.stand = 'product' if product else 'demo'

        _demo_v3 = 'https://markirovka.sandbox.crptech.ru/api/v3/true-api'
        _demo_v4 = 'https://markirovka.sandbox.crptech.ru/api/v4/true-api'
        _prod_v3 = 'https://markirovka.crpt.ru/api/v3/true-api'
        _prod_v4 = 'https://markirovka.crpt.ru/api/v4/true-api'

        self.url_v3 = _prod_v3 if product else _demo_v3
        self.url_v4 = _prod_v4 if product else _demo_v4


    def get_urls(self) -> dict[str]:
        return self.url_v3, self.url_v4, self.stand

class ResponseStatus(Enum):
    OK = (200, "OK", "Статус ответа в случае успеха")
    CREATED = (201, "CREATED", "Статус ответа в случае успеха")
    ACCEPTED = (202, "ACCEPTED", "Статус ответа в случае успеха")
    BAD_REQUEST = (400, "ERROR", "Ошибка в параметрах запроса (отсутствует обязательный параметр)")
    INVALID_PARAM_TYPE = (872, "ERROR", "Ошибка в параметрах запроса (неверный тип параметра)")
    UNAUTHORIZED = (401, "ERROR", "Ошибка авторизации")
    ATTRIBUTIVE_ERROR = (402, "ERROR", "Ошибка в атрибутивном составе тела запроса")
    FORBIDDEN = (403, "ERROR", "Доступ запрещён")
    NOT_FOUND = (404, "ERROR", "Запрашиваемая информация не найдена в ГИС МТ")
    CONFLICT = (409, "ERROR", "Запрос не может быть выполнен из-за конфликтного обращения к ресурсу")
    GONE = (410, "ERROR", "Ресурс ранее был доступен по указанному URL, но сейчас он удалён и недоступен")
    PAYLOAD_TOO_LARGE = (414, "ERROR", "Превышен допустимый размер тела запроса")
    UNPROCESSABLE_ENTITY = (422, "ERROR", "Ошибка проверки подписи")
    INTERNAL_SERVER_ERROR = (500, "ERROR", "Внутренняя ошибка удалённых систем")
    BAD_GATEWAY = (502, "ERROR", "Сервер временно недоступен или заблокирован")
    SERVICE_UNAVAILABLE = (503, "ERROR", "Проблема с доступом к удалённой системе")
    GATEWAY_TIMEOUT = (504, "ERROR", "Ошибка при получении ответа системы")

class DocumentFormat(str, Enum):
    '''
    Формат подачи документа\n
    `MANUAL` - формат *.json\n
    `XML` - формат *.xml\n
    `CSV` - формат *.csv\n
    '''
    MANUAL = 'MANUAL'
    XML = 'XML'
    CSV = 'CSV'

class DocumentTypes(str, Enum):
    '''
    Справочник: Типы документов\n
    [-] `AGGREGATION_DOCUMENT` - Формирование упаковки в формате `.json`\n
    [-] `AGGREGATION_DOCUMENT_XML` - Формирование упаковки в формате `.xml`\n
    [-] `SETS_AGGREGATION` - Формирование наборов в формате `.json`\n
    [-] `SETS_AGGREGATION_XML` - Формирование наборов в формате `.xml`\n
    [-] `DISAGGREGATION_DOCUMENT` - Расформирование упаковки в формате `.json`\n
    [-] `DISAGGREGATION_DOCUMENT_XML` - Расформирование упаковки в формате `.xml`\n
    [-] `REAGGREGATION_DOCUMENT` - Трансформация упаковки в формате `.json`\n
    [-] `REAGGREGATION_DOCUMENT_XML` - Трансформация упаковки в формате `.xml`\n
    [-] `LP_INTRODUCE_GOODS` - Ввод в оборот. Производство РФ в формате `.json`\n
    [-] `LP_INTRODUCE_GOODS_CSV` - Ввод в оборот. Производство РФ в формате `.csv`\n
    [-] `LP_INTRODUCE_GOODS_XML` - Ввод в оборот. Производство РФ в формате `.xml`\n
    [-] `LP_SHIP_GOODS` - Отгрузка в формате `.json`\n
    [-] `LP_SHIP_GOODS_CSV` - Отгрузка в формате `.csv`\n
    [-] `LP_SHIP_GOODS_XML` - Отгрузка в формате `.xml`\n
    [-] `LP_SHIP_GOODS_CROSSBORDER` - Отгрузка при трансграничной торговле в формате `.json`\n
    [-] `EAS_GTIN_CROSSBORDER_EXPORT` - Отгрузка в государствах-членах ЕАЭС с признанием КИ в формате `.json`\n
    [-] `EAS_GTIN_CROSSBORDER_EXPORT_CSV` - Отгрузка в государствах-членах ЕАЭС с признанием КИ в формате `.csv`\n
    [-] `EAS_GTIN_CROSSBORDER_IMPORT` - Отгрузка из государств-членов ЕАЭС с признанием КИ в формате `.json`\n
    [-] `EAS_CROSSBORDER` - Отгрузка из ЕАЭС с признанием КИ в формате `.json`\n
    [-] `REPORT_REWEIGHING` - Отчёт о перевзвешивании в формате `.json`\n
    [-] `LP_ACCEPT_GOODS` - Приёмка в формате `.json`\n
    [-] `LP_ACCEPT_GOODS_XML` - Приёмка в формате `.xml`\n
    [-] `EAS_GTIN_CROSSBORDER_ACCEPTANCE` - Приёмка отгрузки из государств-членов ЕАЭС с признанием КИ в формате `.json`\n
    [-] `EAS_GTIN_CROSSBORDER_ACCEPTANCE_CSV` - Приёмка отгрузки из государств-членов ЕАЭС с признанием КИ в формате `.csv`\n
    [-] `EAS_GTIN_CROSSBORDER_EXPORT_ACCEPTANCE` - Приёмка отгрузки в государствах-членах ЕАЭС с признанием КИ в формате `.json`\n
    [-] `LK_REMARK` - Перемаркировка в формате `.json`\n
    [-] `LK_REMARK_XML` - Перемаркировка в формате `.xml`\n
    [-] `LP_GOODS_IMPORT` - Ввод в оборот. Производство вне ЕАЭС в формате `.json`\n
    [-] `LP_GOODS_IMPORT_XML` - Ввод в оборот. Производство вне ЕАЭС в формате `.xml`\n
    [-] `LP_CANCEL_SHIPMENT` - Отмена отгрузки в формате `.json`\n
    [-] `LP_CANCEL_SHIPMENT_CROSSBORDER` - Отмена отгрузки при трансграничной торговле в формате `.json`\n
    [-] `LK_KM_CANCELLATION` - Списание не нанесённых КИ в формате `.json`\n
    [-] `LK_KM_CANCELLATION_XML` - Списание не нанесённых КИ в формате `.xml`\n
    [-] `LK_APPLIED_KM_CANCELLATION` - Списание нанесённых КИ в формате `.json`\n
    [-] `LK_APPLIED_KM_CANCELLATION_XML` - Списание нанесённых КИ в формате `.xml`\n
    [-] `LK_CONTRACT_COMMISSIONING` - Ввод в оборот товара. Контрактное производство РФ в формате `.json`\n
    [-] `LK_CONTRACT_COMMISSIONING_XML` - Ввод в оборот товара. Контрактное производство РФ в формате `.xml`\n
    [-] `LK_INDI_COMMISSIONING` - Ввод в оборот товара. Полученных от физических лиц в формате `.json`\n
    [-] `LK_INDI_COMMISSIONING_XML` - Ввод в оборот товара. Полученных от физических лиц в формате `.xml`\n
    [-] `LP_RETURN` - Возврат в оборот в формате `.json`\n
    [-] `LP_RETURN_XML` - Возврат в оборот в формате `.xml`\n
    [-] `LP_INTRODUCE_OST` - Ввод в оборот. Маркировка остатков в формате `.json`\n
    [-] `LP_INTRODUCE_OST_XML` - Ввод в оборот. Маркировка остатков в формате `.xml`\n
    [-] `CROSSBORDER` - Ввод в оборот. Трансграничная торговля в формате `.json`\n
    [-] `CROSSBORDER_XML` - Ввод в оборот. Трансграничная торговля в формате `.xml`\n
    [-] `FURS_CROSSBORDER` - Ввод в оборот. Трансграничная торговля («Товары из натурального меха») в формате `.json`\n
    [-] `FURS_CROSSBORDER_XML` - Ввод в оборот. Трансграничная торговля («Товары из натурального меха») в формате `.xml`\n
    [-] `LK_RECEIPT` - Вывод из оборота в формате `.json`\n
    [-] `LK_RECEIPT_CSV` - Вывод из оборота в формате `.csv`\n
    [-] `LK_RECEIPT_XML` - Вывод из оборота в формате `.xml`\n
    [-] `LP_FTS_INTRODUCE` - Ввод в оборот. Импорт с ФТС в формате `.json`\n
    [-] `LP_FTS_INTRODUCE_XML` - Ввод в оборот. Импорт с ФТС в формате `.xml`\n
    [-] `LP_FTS_INTRODUCE_RESPONSE` - Декларация на товары в формате `.json`\n
    [-] `ATK_AGGREGATION` - Формирование АТК в формате `.json`\n
    [-] `ATK_AGGREGATION_XML` - Формирование АТК в формате `.xml`\n
    [-] `ATK_TRANSFORMATION` - Трансформация АТК в формате `.json`\n
    [-] `ATK_TRANSFORMATION_XML` - Трансформация АТК в формате `.xml`\n
    [-] `ATK_DISAGGREGATION` - Расформирование АТК в формате `.json`\n
    [-] `ATK_DISAGGREGATION_XML` - Расформирование АТК в формате `.xml`\n
    [-] `RECEIPT` - Чек (Формируется оператором фискальных данных)\n
    [-] `RECEIPT_RETURN` - Чек возврата (Формируется оператором фискальных данных)\n
    [-] `WRITE_OFF` - Выбытие в формате `.json`\n
    [-] `WRITE_OFF_XML` - Выбытие в формате `.xml`\n
    [-] `EAS_CROSSBORDER_EXPORT` - Отгрузка в ЕАЭС с признанием КИ (экспорт) в формате `.json`\n
    [-] `EAS_CROSSBORDER_EXPORT_CSV` - Отгрузка в ЕАЭС с признанием КИ (экспорт) в формате `.csv`\n
    [-] `EAS_CROSSBORDER_EXPORT_ACCEPTANCE` - Приёмка отгрузки в ЕАЭС с признанием КИ (экспорт) в формате `.json`\n
    [-] `LK_INDIVIDUALIZATION` - Индивидуализация КиЗ («Товары из натурального меха») в формате `.json`\n
    [-] `LK_INDIVIDUALIZATION_XML` - Индивидуализация КиЗ («Товары из натурального меха») в формате `.xml`\n
    [-] `FURS_FTS_INTRODUCE` - Ввод в оборот. Импорт ФТС («Товары из натурального меха») в формате `.json`\n
    [-] `FURS_FTS_INTRODUCE_XML` - Ввод в оборот. Импорт ФТС («Товары из натурального меха») в формате `.xml`\n
    [-] `LK_GTIN_RECEIPT` - Вывод из оборота (ОСУ) в формате `.json`\n
    [-] `LK_GTIN_RECEIPT_CANCEL` - Отмена вывода из оборота (ОСУ) в формате `.json`\n
    [-] `CIS_INFORMATION_CHANGE` - Корректировка сведений о кодах в формате `.json`\n
    [-] `CONNECT_TAP` - Подключение кега к оборудованию для розлива в формате `.json`\n
    [-] `GRAY_ZONE_CSV` - Уведомление о временно непрослеживаемых кодах идентификации (Табачная продукция) в формате `.csv`\n
    '''
    AGGREGATION_DOCUMENT = 'AGGREGATION_DOCUMENT'
    AGGREGATION_DOCUMENT_XML = 'AGGREGATION_DOCUMENT_XML'
    SETS_AGGREGATION = 'SETS_AGGREGATION'
    SETS_AGGREGATION_XML = 'SETS_AGGREGATION_XML'
    DISAGGREGATION_DOCUMENT = 'DISAGGREGATION_DOCUMENT'
    DISAGGREGATION_DOCUMENT_XML = 'DISAGGREGATION_DOCUMENT_XML'
    REAGGREGATION_DOCUMENT = 'REAGGREGATION_DOCUMENT'
    REAGGREGATION_DOCUMENT_XML = 'REAGGREGATION_DOCUMENT_XML'
    LP_INTRODUCE_GOODS = 'LP_INTRODUCE_GOODS'
    LP_INTRODUCE_GOODS_CSV = 'LP_INTRODUCE_GOODS_CSV'
    LP_INTRODUCE_GOODS_XML = 'LP_INTRODUCE_GOODS_XML'
    LP_SHIP_GOODS = 'LP_SHIP_GOODS'
    LP_SHIP_GOODS_CSV = 'LP_SHIP_GOODS_CSV'
    LP_SHIP_GOODS_XML = 'LP_SHIP_GOODS_XML'
    LP_SHIP_GOODS_CROSSBORDER = 'LP_SHIP_GOODS_CROSSBORDER'
    EAS_GTIN_CROSSBORDER_EXPORT = 'EAS_GTIN_CROSSBORDER_EXPORT'
    EAS_GTIN_CROSSBORDER_EXPORT_CSV = 'EAS_GTIN_CROSSBORDER_EXPORT_CSV'
    EAS_GTIN_CROSSBORDER_IMPORT = 'EAS_GTIN_CROSSBORDER_IMPORT'
    EAS_CROSSBORDER = 'EAS_CROSSBORDER'
    REPORT_REWEIGHING = 'REPORT_REWEIGHING'
    LP_ACCEPT_GOODS = 'LP_ACCEPT_GOODS'
    LP_ACCEPT_GOODS_XML = 'LP_ACCEPT_GOODS_XML'
    EAS_GTIN_CROSSBORDER_ACCEPTANCE = 'EAS_GTIN_CROSSBORDER_ACCEPTANCE'
    EAS_GTIN_CROSSBORDER_ACCEPTANCE_CSV = 'EAS_GTIN_CROSSBORDER_ACCEPTANCE_CSV'
    EAS_GTIN_CROSSBORDER_EXPORT_ACCEPTANCE = 'EAS_GTIN_CROSSBORDER_EXPORT_ACCEPTANCE'
    LK_REMARK = 'LK_REMARK'
    LK_REMARK_XML = 'LK_REMARK_XML'
    LP_GOODS_IMPORT = 'LP_GOODS_IMPORT'
    LP_GOODS_IMPORT_XML = 'LP_GOODS_IMPORT_XML'
    LP_CANCEL_SHIPMENT = 'LP_CANCEL_SHIPMENT'
    LP_CANCEL_SHIPMENT_CROSSBORDER = 'LP_CANCEL_SHIPMENT_CROSSBORDER'
    LK_KM_CANCELLATION = 'LK_KM_CANCELLATION'
    LK_KM_CANCELLATION_XML = 'LK_KM_CANCELLATION_XML'
    LK_APPLIED_KM_CANCELLATION = 'LK_APPLIED_KM_CANCELLATION'
    LK_APPLIED_KM_CANCELLATION_XML = 'LK_APPLIED_KM_CANCELLATION_XML'
    LK_CONTRACT_COMMISSIONING = 'LK_CONTRACT_COMMISSIONING'
    LK_CONTRACT_COMMISSIONING_XML = 'LK_CONTRACT_COMMISSIONING_XML'
    LK_INDI_COMMISSIONING = 'LK_INDI_COMMISSIONING'
    LK_INDI_COMMISSIONING_XML = 'LK_INDI_COMMISSIONING_XML'
    LP_RETURN = 'LP_RETURN'
    LP_RETURN_XML = 'LP_RETURN_XML'
    LP_INTRODUCE_OST = 'LP_INTRODUCE_OST'
    LP_INTRODUCE_OST_XML = 'LP_INTRODUCE_OST_XML'
    CROSSBORDER = 'CROSSBORDER'
    CROSSBORDER_XML = 'CROSSBORDER_XML'
    FURS_CROSSBORDER = 'FURS_CROSSBORDER'
    FURS_CROSSBORDER_XML = 'FURS_CROSSBORDER_XML'
    LK_RECEIPT = 'LK_RECEIPT'
    LK_RECEIPT_CSV = 'LK_RECEIPT_CSV'
    LK_RECEIPT_XML = 'LK_RECEIPT_XML'
    LP_FTS_INTRODUCE = 'LP_FTS_INTRODUCE'
    LP_FTS_INTRODUCE_XML = 'LP_FTS_INTRODUCE_XML'
    LP_FTS_INTRODUCE_RESPONSE = 'LP_FTS_INTRODUCE_RESPONSE'
    ATK_AGGREGATION = 'ATK_AGGREGATION'
    ATK_AGGREGATION_XML = 'ATK_AGGREGATION_XML'
    ATK_TRANSFORMATION = 'ATK_TRANSFORMATION'
    ATK_TRANSFORMATION_XML = 'ATK_TRANSFORMATION_XML'
    ATK_DISAGGREGATION = 'ATK_DISAGGREGATION'
    ATK_DISAGGREGATION_XML = 'ATK_DISAGGREGATION_XML'
    RECEIPT = 'RECEIPT'
    RECEIPT_RETURN = 'RECEIPT_RETURN'
    WRITE_OFF = 'WRITE_OFF'
    WRITE_OFF_XML = 'WRITE_OFF_XML'
    EAS_CROSSBORDER_EXPORT = 'EAS_CROSSBORDER_EXPORT'
    EAS_CROSSBORDER_EXPORT_CSV = 'EAS_CROSSBORDER_EXPORT_CSV'
    EAS_CROSSBORDER_EXPORT_ACCEPTANCE = 'EAS_CROSSBORDER_EXPORT_ACCEPTANCE'
    LK_INDIVIDUALIZATION = 'LK_INDIVIDUALIZATION'
    LK_INDIVIDUALIZATION_XML = 'LK_INDIVIDUALIZATION_XML'
    FURS_FTS_INTRODUCE = 'FURS_FTS_INTRODUCE'
    FURS_FTS_INTRODUCE_XML = 'FURS_FTS_INTRODUCE_XML'
    LK_GTIN_RECEIPT = 'LK_GTIN_RECEIPT'
    LK_GTIN_RECEIPT_CANCEL = 'LK_GTIN_RECEIPT_CANCEL'
    CIS_INFORMATION_CHANGE = 'CIS_INFORMATION_CHANGE'
    CONNECT_TAP = 'CONNECT_TAP'
    GRAY_ZONE_CSV = 'GRAY_ZONE_CSV'

