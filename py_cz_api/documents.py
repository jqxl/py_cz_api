import requests

from enum import Enum

from .certificates import Certificate


class Organization:
    inn: str

    def __init__(self, inn:str) -> None:
        self.inn = inn

class Document:
    organization: Organization
    certificate: Certificate

  #{
  #"document_format":"string",
  #"product_document":"<Документ в формате base64>",
  #"type":"string",
  #"signature":"<Открепленная УКЭП формата Base64>"
  #}

    def __init__(self,
                 organization:Organization,
                 certificate: Certificate) -> None:
        self.organization = organization
        self.certificate = certificate
        raise NotImplementedError