from pprint import pprint

import requests as requests
import tqdm as tqdm
from bs4 import BeautifulSoup
import sqlite3
from make_city_dict import cities_dicts

url = f"https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
print(url)
response = requests.get(url)
so = BeautifulSoup(response.text, "html.parser")
con = sqlite3.connect('1.db3')
cur = con.cursor()
dict_of_cities = cities_dicts()
rep_cities = []
r_city = ['']


def values(url):
    url = url
    response = requests.get(url)
    so = BeautifulSoup(response.text, "html.parser")
    data = so.find('div', class_='mw-parser-output').find_all('table')
    for i in data:
        try:
            if 'infobox' in i['class'][1]:
                data = i
                break
        except:
            pass
    coord = data.find_all('span', class_='coordinates plainlinks nourlexpansion')[0].find('span').find('a')[
        'href'].split('/')
    coord[0] = coord[-3]
    coord[1] = coord[-2]
    del coord[2:]
    tr = data.find_all('tr')
    for i in tr:
        if 'км' in i.text:
            try:
                sq = i.find('span').text
            except:
                sq = ''
            break
        else:
            sq = ''
    for i in sq.split(' '):
        if i.isdigit():
            sq = i + ' км²'
    for i in tr:
        if 'UTC' in i.text:
            utc = i.find('span').text
            break
        else:
            utc = ''
    for i in tr:
        if 'Национальности' in i.text:
            national = i.find('td').text
            national = national[1:]
            break
        else:
            national = ''
    for i in tr:
        if 'Официальный язык' in i.text:
            language = i.find('span').text
            break
        else:
            language = ''
    for i in tr:
        if 'Тип климата' in i.text:
            climate = i.find('td').text
            climate = climate.strip()
            break
        else:
            climate = ''
    for i in tr:
        if 'Плотность' in i.text:
            density = i.find('td').text
            density = density.strip()
            break
        else:
            density = ''
    try:
        url_flag = 'https:' + data.find('img', alt='Флаг')['src']
    except:
        url_flag = ''
    try:
        url_gerb = 'https:' + data.find('img', alt='Герб')['src']
    except:
        url_gerb = ''
    return coord, sq, utc, national, language, climate, density, url_gerb, url_flag


for i in so.find("div", class_="mw-parser-output").find('table').find_all('tr')[2:]:
    data = i.find_all('td')
    flag = False
    # url = f"https://google.com/search?q=площадь+города+{data[2].text}"
    # response = requests.get(url)
    # so = BeautifulSoup(response.text, "html.parser")
    if r_city[0] == data[2].text:
        rep_cities += [data[2].text]
        flag = True
    r_city[0] = data[2].text
    # try:
    #     sq = so.select_one('.BNeawe.iBp4i.AP7Wnd').text
    # except:
    #     sq = 'нет площади'
    coord, sq, utc, national, language, climate, density, url_gerb, url_flag = values(
        str('https://ru.wikipedia.org' + str(data[2].find('a')['href'])))
    coord = coord[0] + ' ' + coord[1]
    print(data[2].text)
    if data[2].text in dict_of_cities and not flag:
        coord = dict_of_cities[data[2].text][0] + ' ' + dict_of_cities[data[2].text][1]
    cur.execute(
        """INSERT INTO cities(name, coordinates, population, river, region, federal_district, date, href, square, names, 
        language, time, nationality, flag, gerb, climate, density) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?)""",
        (data[2].text, coord, data[5].text, '1', data[3].text, data[4].text, data[6].find('a').text,
         str('https://ru.wikipedia.org' + str(data[2].find('a')['href'])), sq, data[8].text, language, utc, national,
         url_flag, url_gerb, climate, density))
    con.commit()
con.close()
