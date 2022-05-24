import requests
from bs4 import BeautifulSoup
import pandas
import ExcelExport


# Kiểm tra tình trạng link url
# url: Link trang web muốn kiểm tra, kiểm tra được mọi trang web
# trẩ về một biến boolean là trang web có ổn ko
# trả về kèm theo một string là lỗi gặp phải là gì khi web ko ổn
def is_link_ok(url):
    r = requests.head(url)
    if 200 <= r.status_code < 400:
        return True, "The website is okay. Code: 200"
    elif 400 <= r.status_code < 500:
        return False, "The website can't be found. Code: 4xx"
    elif 500 <= r.status_code:
        return False, "The website server is currently unavailable. Code: 5xx"
    return True, 100


# trả về dữ liệu dạng html của file thời khóa biểu, kiểm tra tình trạng web, kiểm tra tk mk
# 26/4/2022: giờ hàm này cũng trả về thêm một biến boolean để kiểm tra xem quá trình chạy có ok ko
# nếu chạy ko ok thì dữ liệu trả về sẽ là lý do tại sao ko chạy được
# Truyền vào 2 biến, là tài khoản và mật khẩu
# nếu mk và tk là dạng string thì khi truyền vào cần có dấu ""
# Trả về thông tin dạng html bảng thời khóa biểu
# Có kiểm tra sai tk hay mk
# sẽ raise exception khi web trường ko ổn và khi tk hay mk sai
def login(LoginName, Password):
    s = requests.Session()
    url = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'
    is_ok, details = is_link_ok(url)
    while is_ok and details == 100:
        print("Please Wait. Code: 1xx")
        is_ok, details = is_link_ok(url)
    if not is_ok:
        # Exception khi web trường ko vào được
        return False, details
    g = s.get(url)
    token = BeautifulSoup(g.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'})['value']
    payload = {'LoginName': LoginName,
               'Password': Password,
               '__RequestVerificationToken': token}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        auth = s.post(url, data=payload, headers=headers, timeout=30)
    except requests.Timeout as error:
        return False, "Timeout, the website takes too long to respond"
    if not auth.text.__contains__("Chào mừng:"):
        # Exception khi sai tk hay mk
        return False, "Username or Password is incorrect!"
    if auth.text.__contains__("Không tìm thấy môn học!"):
        return False, "There's no table to collect data from!"
    payload2 = {'layout': 'main'}
    try:
        s.get('http://dangkyhoc.vnu.edu.vn/xem-va-in-ket-qua-dang-ky-hoc/1?layout=main', data=payload2, timeout=30)
    except requests.Timeout as error:
        return False, "Timeout, the website takes too long to respond"
    res = s.get('http://dangkyhoc.vnu.edu.vn/xuat-ket-qua-dang-ky-hoc/1')
    return True, res


# trả về dữ liệu dưới dạng các object trong một list mới với tên là Subject
# html_text là truyền vào dữ liệu html của bảng cần tách dữ liệu
# hàm trả về subject_list là một list các biến Subject chứa dữ liệu
def table_extract(html_text):
    table_list = pandas.read_html(html_text.content, encoding='utf-8')
    table = table_list[2]
    subject_list = []
    for i in range(len(table.index) - 1):
        time = table.iloc[i, 8]
        time = time.split(" - ", 2)
        subject = ExcelExport.Subject(table.iloc[i, 2], table.iloc[i, 6], table.iloc[i, 7], int(time[0]), int(time[1]),
                                      table.iloc[i, 9])
        subject_list.append(subject)
    return subject_list


# giờ đây hàm này sẽ phụ trách các cái lỗi xảy ra khi chạy
# hàm login giờ sẽ trả về 2 biến, một biến là data và một biến là bool
# nếu trả về true thì vẫn như bình thường dữ liệu trang web các thứ
# nếu trả về false thì data được kèm theo sẽ là tên lỗi
# mọi người có đổi thay vì in ra thì nó sẽ trả về lỗi
# nhưng mà làm như này thì sau khi nó trả về sẽ phải viết các hàm
# kiểm tra xem đó là lỗi hay đó là data
def login_protocol(Username, Password):
    if Username is None or Password is None:
        return False, "Username and Password can not be empty"
    else:
        return login(Username, Password)


# Testing zone
tk = "tk"
mk = "mk"
is_ok, data = login_protocol(tk, mk)
if not is_ok:
    print(data)
else:
    Subject_list = table_extract(data)
    print(ExcelExport.html_table(Subject_list))
