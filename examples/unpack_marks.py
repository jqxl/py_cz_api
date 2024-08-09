import py_cz_api
import pandas as pd

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.ApiExtended(token, py_cz_api.Pgs.ncp)

mark_list = [
'00046102182002270072',
'00046102182002270089',
'00046102182002270096',
'00046102182002270065'
]

cis_col = 'cis'
df = pd.DataFrame({'cis': mark_list})

df_unpacked = api.df_recursive_unpack(df, 'cis')
print(df_unpacked)