import xlsxwriter
import random


# Tạo Object mới để lưu toàn bộ dữ liệu cần thiết của môn học
# Object này cần truyền vào
# name: tên môn học
# classCode: mã môn học
# date: Học vào thứ mấy
# start: tiết học bắt đầu là tiết thứ mấy
# end: tiết học cuối là tiết thứ mấy
# where: học tại lớp nào
# bg_color, font_color: màu của nền và màu cửa chữ, vẫn đang thử nghiệm chưa làm xong
# hiện tại đang để màu chữ là màu trắng và màu nền là random
class Subject:
    def __init__(self, name, classCode, date, start, end, where):
        self.name = name
        self.classCode = classCode
        self.date = date
        self.start = start
        self.end = end
        self.where = where
        self.bg_color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        self.font_color = "white"

    # Hàm để trả về dữ liệu cần thiết để điền vào file excel
    # Hàm này là để dễ dàng điền các dữ liệu liên quan đến môn học vào các ô của excel
    def return_data(self):
        return self.name + "\n" + self.classCode + "\n" + self.where


# Object xử lý việc tạo bảng excel, truyền vào tên file mong muốn
# Truyền vào name: tên của file excel mà mình muốn đặt
# worksheet: trang tính mà mình đang làm việc với
class Schedule:
    def __init__(self, name):
        self.worktable = xlsxwriter.Workbook(name + ".xlsx")
        self.worksheet = self.worktable.add_worksheet()

    # Tạo các giá trị tối thiểu của một file tkb dưới dạng excel
    # Tạo thêm các giá trị như chữ in đậm, căn giữa cho các ô
    def create_frame_work(self):
        bold = self.worktable.add_format({'bold': True})
        bold.set_align('center')
        bold.set_align('vcenter')
        self.worksheet.write('A1', 'Tiết', bold)
        self.worksheet.write('B1', 'Thời gian học', bold)
        for i in range(2, 16):
            self.worksheet.set_row(i - 1, 40)
            self.worksheet.write("A" + str(i), i - 1, bold)
            # Thời gian các tiết
            time = str(i + 5) + "h00' - " + str(i + 5) + "h50'"
            self.worksheet.write("B" + str(i), time, bold)
        j = 2
        for i in range(ord('C'), ord('H') + 1):
            self.worksheet.write(chr(i) + str(1), "Thứ " + str(j), bold)
            j += 1
        self.worksheet.set_column('A:A', 3)
        self.worksheet.set_column('B:B', 15)
        self.worksheet.set_column('C:H', 25.0)

    # Truyền vào một môn học tại một vị trí của bảng
    # Truyền vào từng biến Subject một, không truyền thẳng list vào
    def insert_subject(self, subject):
        colum = int(subject.date[1])
        row_start = subject.start + 1
        row_end = subject.end + 1
        char = 'A'
        merge_range = chr(ord(char) + colum) + str(row_start) + ":" + chr(ord(char) + colum) + str(row_end)
        cell_data = subject.return_data()
        merge_format = self.worktable.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': 'true',
            'border': 1,
            'bold': True
        })
        merge_format.set_font_color(subject.font_color)
        merge_format.set_bg_color(subject.bg_color)
        self.worksheet.merge_range(merge_range, cell_data, merge_format)
