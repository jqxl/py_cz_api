from base64 import b64encode
from datetime import datetime

import sys
if sys.platform == 'win32':
    from win32com.client import Dispatch
else:
    Dispatch = None

def show_certs() -> dict:
    '''Выводит установленные сертификаты в хранилище

:return dict: {СерийныйНомер:Объект}'''
    # 2 - Current User Store, 'My' - Personal Certificates, 2 - Read mode
    Store = Dispatch('CAdESCOM.Store')
    Store.Open(2, 'My', 2)
    cert_dict = {cert.serialnumber: cert.SubjectName for cert in Store.Certificates}
    Store.Close
    return cert_dict

def _find_Cert(serialnumber: str):
    Store = Dispatch('CAdESCOM.Store')
    Store.Open(2, 'My', 2)
    Cert = next((cert for cert in Store.Certificates if cert.SerialNumber == serialnumber.upper()), None)
    if Cert is None:
        raise KeyError('Сертификат не найден')
    Store.Close()
    return Cert

class Certificate:
    '''Класс с объектом сертификата ЭП, служащий для шифрования данных подписью'''
    def __init__(self, serialnumber: str):
        '''### Требуется:
- КриптоПро SCP
- Установленный Сертификат в личное хранилище
- Контейнер с записанными ключами шифрованиями

:param serialnumber: Серийный номер ЭП. пример: `01EB1AA50033B12D894A535821B96C26C0`
'''
        self.CertObj = _find_Cert(serialnumber)
        self.serialnumber = serialnumber.upper()
        self.owner = self.CertObj.SubjectName

    def __repr__(self) -> str:
        return f'Lib: cz_api Class: Certificate\nserialnumber: {self.serialnumber}\nowner: {self.owner}'

    def sign_data(self, data: str, encoding: str = 'ascii') -> str:
        '''Шифрует входящий текст в Base64'''

        Signer = Dispatch('CAdESCOM.CPSigner')
        Signer.Certificate = self.CertObj
        Signing_attr = Dispatch('CAdESCOM.CPAttribute')
        Signing_attr.Name = 0
        Signing_attr.Value = datetime.now()
        Signer.AuthenticatedAttributes2.Add(Signing_attr)
        signed_data = Dispatch('CAdESCOM.CadesSignedData')
        signed_data.ContentEncoding = 1

        data_bytes = data.encode(encoding)
        base64_bytes = b64encode(data_bytes)
        base64_data = base64_bytes.decode(encoding)
        signed_data.Content = base64_data
        encrypted_str = signed_data.SignCades(Signer, 1, False, 0)
        return encrypted_str
