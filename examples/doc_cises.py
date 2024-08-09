import py_cz_api

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.Api(token, py_cz_api.Pgs.ncp)

doc_id = '5e74c9bb-5bd5-4fc0-9d0e-6705d5c146cd'

ans = api.doc_cises(doc_id)

print(ans)
