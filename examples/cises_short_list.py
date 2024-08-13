import py_cz_api

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.Api(token, py_cz_api.Pgs.ncp)

mark_list = ['01230000157926=Mflh=dAAAA']

ans = api.cises_short_list(mark_list)

print(ans)