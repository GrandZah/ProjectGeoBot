import os
import time

import requests
from PIL import Image
from threading import Thread


def image_to_black_map(true_city, dict_of_cities, i_size, name):
    # ПЕРВОЕ
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={dict_of_cities[true_city][1]},{dict_of_cities[true_city][0]}" \
                  f"&z={i_size}&l=skl&scale=1"
    response = requests.get(map_request)
    map_file = f"static/img/{true_city}_{i_size}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # ВТОРОЕ
    w = Thread(target=p1, args=(true_city, dict_of_cities, i_size, name))
    q = Thread(target=p2, args=(true_city, dict_of_cities, i_size, name))
    w.start()
    q.start()
    w.join()
    q.join()


def p1(true_city, dict_of_cities, i_size, name):
    img = Image.open(f"static/img/{true_city}_{i_size}.png")
    x, y = img.size
    pixels = img.load()
    for i in range(x // 2):
        for j in range(y):
            r, g, b = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
            if r in [i for i in range(230, 256)] and g in [i for i in range(230, 256)] and b in [i for i in
                                                                                                 range(230, 256)]:
                r, g, b = 0, 0, 0
            else:
                r, g, b = 255, 255, 255
            pixels[i, j] = r, g, b
    # img.save(f"static/img/{true_city}_{i_size}_1.png")
    img_0 = Image.open(f"static/img/{true_city}_{name}.png")
    pixels_10 = img_0.load()
    for i in range(x // 2):
        for j in range(y):
            r_black, g_black, b_black = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]

            if r_black == 0:  # Если видим черную точку то закрышиваем квадрат 10 на 10 около этой точки
                for s in range(-5, 5):  # В радиусе -+ 5
                    for k in range(-5, 5):
                        if 0 < i + s < x and 0 < j + k < y:  # проверяем что оно вообще есть
                            pixels_10[i + s, j + k] = pixels_10[i, j]  # Выбираем цвет (У Москвы 3 цвета даже)
    img_0.save(f"static/img/{true_city}_{i_size}_1.png")


def p2(true_city, dict_of_cities, i_size, name):
    img = Image.open(f"static/img/{true_city}_{i_size}.png")
    x, y = img.size
    pixels = img.load()
    for i in range(x // 2 + 1, x):
        for j in range(y):
            r, g, b = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
            if r in [i for i in range(230, 256)] and g in [i for i in range(230, 256)] and b in [i for i in
                                                                                                 range(230, 256)]:
                r, g, b = 0, 0, 0
            else:
                r, g, b = 255, 255, 255
            pixels[i, j] = r, g, b
    img_10 = Image.open(f"static/img/{true_city}_{name}.png")
    pixels = img.load()
    pixels_10 = img_10.load()
    for i in range(x // 2 + 1, x):
        for j in range(y):
            r_black, g_black, b_black = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]

            if r_black == 0:  # Если видим черную точку то закрышиваем квадрат 10 на 10 около этой точки
                for s in range(-5, 5):  # В радиусе -+ 5
                    for k in range(-5, 5):
                        if 0 < i + s < x and 0 < j + k < y:  # проверяем что оно вообще есть
                            pixels_10[i + s, j + k] = pixels_10[i, j]  # Выбираем цвет (У Москвы 3 цвета даже)
    img_10.save(f"static/img/{true_city}_{i_size}_2.png")


def pt(true_city, dict_of_cities, i_size, name):
    image_to_black_map(true_city, dict_of_cities, i_size, name)
    x, y = Image.open(f"static/img/{true_city}_{name}.png").size[0], \
           Image.open(f"static/img/{true_city}_{name}.png").size[1]
    img = Image.new('RGB', (x, y))
    img_1 = Image.open(f"static/img/{true_city}_{i_size}_1.png")
    img_2 = Image.open(f"static/img/{true_city}_{i_size}_2.png")
    im_crop = img_1.crop((0, 0, x // 2, y))
    im_crop_2 = img_2.crop((x // 2 + 1, 0, x, y))
    img.paste(im_crop, (0, 0))
    img.paste(im_crop_2, (x // 2, 0))
    img.save(f"static/img/{true_city}_{name}.png")
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        f'static/img/{true_city}_{i_size}_2.png')
    os.remove(path)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        f'static/img/{true_city}_{i_size}_1.png')
    os.remove(path)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        f'static/img/{true_city}_{i_size}.png')
    os.remove(path)
