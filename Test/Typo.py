# File này được dùng để thử các hàm và các code trước khi code thật vào hàm chính

String = 'T4'
row_start = 7
row_end = 9
colum = int(String[1])
char = 'A'
cell_to_merge_start = chr(ord(char) + colum) + str(row_start)
cell_to_merge_end = chr(ord(char) + colum) + str(row_end)
print(cell_to_merge_start)
print(cell_to_merge_end)
