import py_cz_api
import pandas as pd

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.ApiExtended(token, py_cz_api.Pgs.ncp)

doc = 'ON_NSCHFDOPPRMARK_2be241ee8c99aae445c9917226eb52b81df_2BM-9729308375-771401001-202311220641472597668_20240807_b5f64dcf-eb95-4461-b19c-f748952fb16a'
ans = api.doc_info(doc, body=True)
print(ans)
