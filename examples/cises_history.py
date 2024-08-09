import py_cz_api
import pandas as pd

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.Api(token, py_cz_api.Pgs.ncp)

mark = '010461021820626021S4Zsj5h'

answer = api.cises_history(mark)
print(pd.json_normalize(answer))