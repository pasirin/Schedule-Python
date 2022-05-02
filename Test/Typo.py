import requests

s = requests.Session()
url = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'
try:
    g = s.get(url, timeout=0.000000001)
except requests.Timeout as error:
    print(error)