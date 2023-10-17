from random import choice

import requests


def image_make_norm(true_city, dict_of_cities, i_size):
    name = choice(['спутнику', 'карте'])
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={dict_of_cities[true_city][1]},{dict_of_cities[true_city][0]}" \
                  f"&z={i_size}&l={'sat' if name == 'спутнику' else 'map'}"
    response = requests.get(map_request)
    map_file = f"static/img/{true_city}_{name}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return name