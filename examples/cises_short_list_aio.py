import py_cz_api
import asyncio

essep = '01EB1AA50033B12D894A535821B96C26C0'
certificate = py_cz_api.Certificate(essep)
token = py_cz_api.Token.create_from_cert(certificate)
api = py_cz_api.Api(token, py_cz_api.Pgs.ncp)

def main():
    mark_list = ['01230000157926=Mflh=dAAAA']

    ans = api.cises_short_list_aio(mark_list)
    return ans

if __name__ == '__main__':
    ans = asyncio.run(main())
    print(ans)
