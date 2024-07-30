from base64 import b64encode
from win32com.client import Dispatch
from datetime import datetime

def show_certs() -> dict:
    '''Возвращает сертификаты вида {СерийныйНомер:Объект}'''
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
        '''Поддерживаются только сертификаты из личного хранилища
        См. исходный код Store.Open(*, 'My', *)'''
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