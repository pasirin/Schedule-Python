import random


# File này được dùng để thử các hàm và các code trước khi code thật vào hàm chính
def font_color(bg_color):
    extract = bg_color.strip('#')
    amount = len(extract)
    list_rgb = list(float(int(extract[i:i + amount // 3], 16)) for i in range(0, amount, amount // 3))
    for i in list_rgb:
        print(i)
    for i in range(len(list_rgb)):
        list_rgb[i] = list_rgb[i]/255
        if list_rgb[i] <= 0.03928:
            list_rgb[i] /= 12.92
        else:
            list_rgb[i] = pow(((list_rgb[i] + 0.055) / 1.055), 2.4)
    for i in list_rgb:
        print(i)
    l = 0.2126 * list_rgb[0] + 0.7152 * list_rgb[1] + 0.0722 * list_rgb[2]
    print(l)


bg_color = "#ffffff"
font_color(bg_color)
