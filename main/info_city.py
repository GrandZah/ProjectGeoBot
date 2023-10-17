import os

import requests
from PIL import Image
from bs4 import BeautifulSoup
from random import choices, sample
from tqdm import tqdm
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
import sqlite3
from make_city_dict import cities_dicts
from datetime import datetime, timedelta
from corr_img_for_cities import correct_img


def info(c, user_id):
    url = f'https://yandex.ru/images/search?text={c}(город)'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    tables = soup.find_all('img', {'class': "serp-item__thumb justifier__thumb"})
    for i in range(4):
        urll = 'https:' + tables[i]['src']
        response = requests.get(urll)
        with open(f'{user_id}_{i}.png', 'wb') as f:
            f.write(response.content)


def info_gerb_flag(user_id, flag, gerb):
    try:
        response = requests.get(flag)
    except:
        response = ''
    try:
        response_2 = requests.get(gerb)
    except:
        response_2 = ''
    if response:
        with open(f'{user_id}_flag.jpg', 'wb') as f:
            f.write(response.content)
            f.close()
    if response_2:
        with open(f'{user_id}_gerb.jpg', 'wb') as f:
            f.write(response_2.content)
            f.close()


def img_ok(user_id, flag, gerb, messages):
    p = Thread(target=info, args=(messages[user_id]['cities']["true_city"], user_id))
    # o = Thread(target=info_gerb_flag, args=(user_id, flag, gerb))
    p.start()
    # o.start()
    p.join()
    # o.join()
    img_0 = Image.open(f'{user_id}_0.png')
    img_01 = Image.open(f'{user_id}_1.png')
    img_02 = Image.open(f'{user_id}_2.png')
    img_03 = Image.open(f'{user_id}_3.png')
    try:
        img_flag = Image.open(f'{user_id}_flag.jpg')
    except:
        img_flag = ''
    try:
        img_gerb = Image.open(f'{user_id}_gerb.jpg')
    except:
        img_gerb = ''
    if img_flag:
        if img_gerb:
            x_f = img_flag.size[0] + 3 + img_gerb.size[0]
            y_f = max(img_flag.size[1], img_gerb.size[1])
            image_flag_gerb = Image.new('RGB', (x_f, y_f), (255, 255, 255))
            image_flag_gerb.paste(img_flag, (0, 0))
            image_flag_gerb.paste(img_gerb, (img_flag.size[0]+3, 0))
            image_flag_gerb.save(f'{user_id}_flag.jpg', quality=1000)

        else:
            x_f = img_flag.size[0]
            y_f = img_flag.size[1]
            image_flag_gerb = Image.new('RGB', (x_f, y_f), (255, 255, 255))
            image_flag_gerb.paste(img_flag, (0, 0))
            image_flag_gerb.save(f'{user_id}_flag.jpg', quality=1000)
    elif img_gerb:
        x_f = img_gerb.size[0]
        y_f = img_gerb.size[1]
        image_flag_gerb = Image.new('RGB', (x_f, y_f), (255, 255, 255))
        image_flag_gerb.paste(img_gerb, (0, 0))
        image_flag_gerb.save(f'{user_id}_flag.jpg', quality=1000)
    try:
        img_gerb.close()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'{user_id}_gerb.jpg')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
        os.remove(path)
    except:
        pass
    # x = max(img_0.size[0] + img_01.size[0], img_02.size[0] + img_03.size[0]) + 3
    # y = max(img_0.size[1], img_02.size[1]) + max(img_01.size[1], img_03.size[1]) + 3
    # img = Image.new('RGB', (x, y), (255, 255, 255))
    # img.paste(img_0, (0, 0))
    # img.paste(img_01, (img_0.size[0]+3, 0))
    # img.paste(img_02, (0, img_0.size[1] + 3))
    # img.paste(img_03, (max(img_02.size[0], img_0.size[0]) + 3, max(img_01.size[1], img_03.size[1]) + 3))
    # img.save(f'{user_id}.png')
    # for i in range(4):
    #     path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
    #                         f'{user_id}_{i}.png')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
    #     os.remove(path)
    correct_img(user_id, img_0, img_01, img_02, img_03)


def text_about(city):
    con = sqlite3.connect('1.db3')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM cities
                            WHERE name == (?)""", (city,)).fetchall()
    if len(result) == 0:
        return 'Информации не найдено(', f'https://ru.wikipedia.org/wiki/{city}', '', ''
    dict_of_cities = cities_dicts()
    if len(result) > 1:
        result = cur.execute("""SELECT * FROM cities
                                WHERE name == (?) and coordinates = (?)""", (city, dict_of_cities[city][0]+' '+dict_of_cities[city][1])).fetchall()
    txt = []
    columns = cur.description
    column = {'id': 'id', 'name': 'Название города', 'coordinates': 'Координаты', 'population': 'Численность населения',
              'river': 'Близлежащая река', 'region': 'Регион', 'federal_district': 'Федеральный округ',
              'date': 'Дата основания', 'href': 'ссылка в сибирь', 'square': 'Площадь', 'time': 'Часовой пояс',
              'language': 'Офф язык', 'nationality': 'Национальности', 'climate': 'Климатический пояс',
              'density': 'Плотность', 'names': 'Прошлые названия'}
    result = list(result[0])
    for i in range(len(result)):
        if i in [0, 1, 2, 4, 5, 6, 8, 14, 15, 9, 17]:
            continue
        if result[i]:
            if '[' in str(result[i]):
                result[i] = result[i][:result[i].index('[')] + result[i][result[i].index(']')+1:]
            if columns[i][0] == 'time':
                hrs = int(result[i].split('+')[1].split(':')[0])
                txt.append(f'{column[columns[i][0]]}: {(datetime.now() + timedelta(hours=hrs-3)).strftime("%H:%M")} - {result[i]}')
            else:
                txt.append(f'{column[columns[i][0]]}: {result[i]}')
    text = result[1] + ', ' + result[5] + ', ' + result[6] + ' ФО' + '\n'
    return text + '\n'.join(txt), result[8], result[14], result[15]
