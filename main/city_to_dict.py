import time
from random import sample, randint, choice

from image_make_norm import image_make_norm
from image_to_black_map_1 import pt
from make_city_dict import cities_dicts


def city_to_dict():
    dict_of_cities = cities_dicts()
    city_1, city_2, city_3, city_4 = sample(list(dict_of_cities.keys()), 4)
    true_city = choice([city_1, city_2, city_3, city_4])
    cities = [city_1, city_2, city_3, city_4]
    i_size = '12'
    name = image_make_norm(true_city, dict_of_cities, i_size)

    if name == 'спутнику':
        return true_city, name, cities
    else:
        pt(true_city, dict_of_cities, i_size, name)
        return true_city, name, cities
