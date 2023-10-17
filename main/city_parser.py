import requests
from bs4 import BeautifulSoup
from random import choices, sample
from tqdm import tqdm
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

t0 = time.time()
response = requests.get("https://time-in.ru/coordinates/russia?")
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all('a', {'class': "coordinates-items-left"})
for item in tqdm(range(len(tables))):
    tables[item] = tables[item]["href"]
dikt = {}
pool = ThreadPool()
q = sample(tables, k=300)
response = pool.map(requests.get, q)
for i in tqdm(range(300)):
    # response = requests.get(f"{i}")
    soup = BeautifulSoup(response[i].text, "html.parser")
    t = soup.find('div', {'class': ""}).text.split(':')[1].split(',')
    t[0], t[1] = t[0][1:], t[1][1:]
    r = soup.find_all('span', {'class': ""})[5].text
    dikt[f"{r}"] = t
dict = dikt

