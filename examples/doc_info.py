import py_cz_api
import pandas as pd

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.ApiExtended(token, py_cz_api.Pgs.ncp)

doc = '621611b1-e776-4d12-8d45-4267a493bb5b'
ans = api.doc_info(doc)
print(ans)
