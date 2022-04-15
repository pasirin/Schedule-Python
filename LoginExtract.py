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
        raise Exception(details)
    g = s.get(url)
    token = BeautifulSoup(g.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'})['value']
    payload = {'LoginName': LoginName,
               'Password': Password,
               '__RequestVerificationToken': token}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    auth = s.post(url, data=payload, headers=headers)
    if not auth.text.__contains__("Chào mừng:"):
        # Exception khi sai tk hay mk
        raise Exception("Username or Password is incorrect!")
    s.post(url, data=payload, headers=headers)
    payload2 = {'layout': 'main'}
    s.get('http://dangkyhoc.vnu.edu.vn/xem-va-in-ket-qua-dang-ky-hoc/1?layout=main', data=payload2)
    res = s.get('http://dangkyhoc.vnu.edu.vn/xuat-ket-qua-dang-ky-hoc/1')
    return res


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


# Thử code ở đây
# Example:
# đăng nhập bằng tk và mk
#
# data = login(tk, mk)
#
# Truyền dữ liệu bảng vào trong hàm tách dữ liệu
#
# Subject_list = table_extract(data)
#
# tạo một bảng excel với tên là "prototype"
#
# schedule = ExcelExport.Schedule("prototype")
#
# tạo những dự liệu cơ bản của một file tkb (ngày, tiết, giờ,...)
#
# schedule.create_frame_work()
#
# hiện tại vì mình chưa làm hàm trung gian nên nếu muốn cho
# các môn học vào bảng thì sẽ phải cho từng môn một trong list như sau
#
# for x in range(len(Subject_list)):
#     schedule.insert_subject(Subject_list[x])
#
# Hàm này là đóng lại bảng excel và hoàn lưu lại thay đổi
# schedule.worktable.close()
