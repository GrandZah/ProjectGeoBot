# from city_parser import dict

def cities_dicts():
    dict_of_cities = {'Москва': ['55.7522', '37.6156'], 'Абакан': ['53.7156', '91.4292'],
                      'Адлер': ['43.429', '39.9239'],
                      'Азов': ['47.1078', '39.4165'], 'Александров': ['56.3952', '38.7122'],
                      'Алексин': ['54.505', '37.0674'],
                      'Альметьевск': ['54.9044', '52.3154'], 'Анадырь': ['64.7342', '177.51'],
                      'Анапа': ['44.8908', '37.3239'],
                      'Ангарск': ['52.5367', '103.886'], 'Анжеро-Судженск': ['56.081', '86.0285'],
                      'Апатиты': ['67.5641', '33.4031'], 'Арзамас': ['55.3949', '43.8399'],
                      'Армавир': ['44.9892', '41.1234'],
                      'Арсеньев': ['44.1525', '133.278'], 'Артём': ['43.3595', '132.189'],
                      'Архангельск': ['64.5401', '40.5433'],
                      'Асбест': ['57.0099', '61.4578'], 'Астрахань': ['46.3497', '48.0408'],
                      'Ачинск': ['56.2694', '90.4993'],
                      'Балаково': ['52.0278', '47.8007'], 'Балахна': ['56.4899', '43.6011'],
                      'Балашиха': ['55.8094', '37.9581'],
                      'Балашов': ['51.5502', '43.1667'], 'Барнаул': ['53.3606', '83.7636'],
                      'Батайск': ['47.1398', '39.7518'],
                      'Белгород': ['50.6107', '36.5802'], 'Белебей': ['54.1167', '54.1167'],
                      'Белово': ['54.4165', '86.2976'],
                      'Белогорск': ['50.9164', '128.477'], 'Белорецк': ['53.9631', '58.3981'],
                      'Белореченск': ['44.7713', '39.8788'], 'Бердск': ['54.7551', '83.0967'],
                      'Березники': ['59.4091', '56.8204'], 'Берёзовский': ['55.6', '86.2'],
                      'Бийск': ['52.5364', '85.2072'],
                      'Биробиджан': ['48.7928', '132.924'], 'Благовещенск': ['50.2796', '127.54'],
                      'Бор': ['56.3581', '44.0748'],
                      'Борисоглебск': ['51.3671', '42.0849'], 'Боровичи': ['58.3878', '33.9155'],
                      'Братск': ['56.1325', '101.614'], 'Брянск': ['53.2521', '34.3717'],
                      'Бугульма': ['54.5378', '52.7985'],
                      'Бугуруслан': ['53.6554', '52.442'], 'Будённовск': ['44.7839', '44.1658'],
                      'Бузулук': ['52.7807', '52.2635'], 'Буйнакск': ['42.819', '47.1192'],
                      'Великие Луки': ['56.34', '30.5452'],
                      'Великий Новгород': ['58.5213', '31.271'], 'Верхняя Пышма': ['56.9705', '60.5822'],
                      'Видное': ['55.5524', '37.7097'], 'Владивосток': ['43.1056', '131.874'],
                      'Владикавказ': ['43.0367', '44.6678'], 'Владимир': ['56.1366', '40.3966'],
                      'Волгоград': ['48.7194', '44.5018'], 'Волгодонск': ['47.5136', '42.1514'],
                      'Волжск': ['55.8664', '48.3594'],
                      'Волжский': ['48.7858', '44.7797'], 'Вологда': ['59.2239', '39.884'],
                      'Вольск': ['52.0454', '47.3799'],
                      'Воркута': ['67.4988', '64.0525'], 'Воронеж': ['51.672', '39.1843'],
                      'Воскресенск': ['55.3173', '38.6526'],
                      'Восточное Дегунино': ['55.8801', '37.5576'], 'Воткинск': ['57.0486', '53.9872'],
                      'Выборг': ['60.7076', '28.7528'], 'Выкса': ['55.3175', '42.1744'],
                      'Вышний Волочек': ['57.5913', '34.5645'],
                      'Вязьма': ['55.2104', '34.2951'], 'Гатчина': ['59.5764', '30.1283'],
                      'Геленджик': ['44.5622', '38.0848'],
                      'Георгиевск': ['44.1519', '43.4697'], 'Глазов': ['58.1393', '52.658'],
                      'Горно-Алтайск': ['51.9606', '85.9189'], 'Грозный': ['43.312', '45.6889'],
                      'Губкин': ['51.2817', '37.5458'],
                      'Гуково': ['48.0621', '39.9355'], 'Гусь-Хрустальный': ['55.6111', '40.6519'],
                      'Дербент': ['42.0678', '48.2899'], 'Дзержинск': ['56.2414', '43.4554'],
                      'Димитровград': ['54.2139', '49.6184'], 'Дмитров': ['56.3448', '37.5204'],
                      'Долгопрудный': ['55.9496', '37.5018'], 'Домодедово': ['55.4413', '37.7537'],
                      'Донецк': ['48.3396', '39.9595'], 'Дубна': ['56.7333', '37.1667'],
                      'Егорьевск': ['55.3828', '39.0323'],
                      'Ейск': ['46.7055', '38.2739'], 'Екатеринбург': ['56.8519', '60.6122'],
                      'Елабуга': ['55.7613', '52.0649'],
                      'Елец': ['52.6237', '38.5017'], 'Ессентуки': ['44.0444', '42.8606'],
                      'Железногорск': ['52.331', '35.3711'],
                      'Железнодорожный': ['55.744', '38.0168'], 'Жигулевск': ['53.3997', '49.4953'],
                      'Жуковский': ['55.5953', '38.1203'], 'Заречный': ['53.2036', '45.1923'],
                      'Заринск': ['53.7074', '84.9493'],
                      'Зеленогорск': ['56.1124', '94.5985'], 'Зеленоград': ['55.9825', '37.1814'],
                      'Зеленодольск': ['55.8438', '48.5178'], 'Златоуст': ['55.1711', '59.6508'],
                      'Иваново': ['56.9972', '40.9714'], 'Ивантеевка': ['55.9711', '37.9208'],
                      'Ижевск': ['56.8498', '53.2045'],
                      'Иркутск': ['52.2978', '104.296'], 'Искитим': ['54.6366', '83.3045'],
                      'Ишим': ['56.1128', '69.4902'],
                      'Ишимбай': ['53.4545', '56.0415'], 'Йошкар-Ола': ['56.6388', '47.8908'],
                      'Казань': ['55.7887', '49.1221'],
                      'Калининград': ['54.7065', '20.511'], 'Калуга': ['54.5293', '36.2754'],
                      'Каменск': ['48.3178', '40.2595'],
                      'Каменск-Уральский': ['56.4185', '61.9329'], 'Камышин': ['50.0983', '45.416'],
                      'Канск': ['56.2017', '95.7175'], 'Каспийск': ['42.8816', '47.6392'],
                      'Кемерово': ['55.3333', '86.0833'],
                      'Кизляр': ['43.8471', '46.7145'], 'Кимры': ['56.8667', '37.35'],
                      'Кингисепп': ['59.3733', '28.6134'],
                      'Кинешма': ['57.4391', '42.1289'], 'Кириши': ['59.4471', '32.0205'],
                      'Киров': ['58.5966', '49.6601'],
                      'Кирово-Чепецк': ['58.5539', '50.0399'], 'Киселёвск': ['53.99', '86.6621'],
                      'Кисловодск': ['43.9133', '42.7208'], 'Климовск': ['55.3635', '37.5298'],
                      'Клин': ['56.3333', '36.7333'],
                      'Клинцы': ['52.7602', '32.2393'], 'Ковров': ['56.3572', '41.3192'],
                      'Когалым': ['62.2654', '74.4791'],
                      'Коломна': ['55.0794', '38.7783'], 'Колпино': ['59.7507', '30.5886'],
                      'Комсомольск-на-Амуре': ['50.5503', '137.01'], 'Копейск': ['55.1172', '61.6282'],
                      'Королёв': ['55.9142', '37.8256'], 'Кострома': ['57.7665', '40.9269'],
                      'Котлас': ['61.2575', '46.6496'],
                      'Красногорск': ['55.8204', '37.3302'], 'Краснодар': ['45.0448', '38.976'],
                      'Краснокаменск': ['50.0979', '118.037'], 'Краснокамск': ['58.0796', '55.7552'],
                      'Краснотурьинск': ['59.7666', '60.2086'], 'Красноярск': ['56.0184', '92.8672'],
                      'Кропоткин': ['45.4375', '40.5756'], 'Крымск': ['44.9293', '37.9912'],
                      'Кстово': ['56.1473', '44.1979'],
                      'Кузнецк': ['53.1167', '46.6004'], 'Кумертау': ['52.7667', '55.7833'],
                      'Кунгур': ['57.4368', '56.9593'],
                      'Курган': ['55.45', '65.3333'], 'Курск': ['51.7373', '36.1874'], 'Кызыл': ['51.7147', '94.4534'],
                      'Лабинск': ['44.6342', '40.7356'], 'Лениногорск': ['54.6026', '52.4609'],
                      'Ленинск-Кузнецкий': ['54.6567', '86.1737'], 'Лесной': ['57.6198', '63.0784'],
                      'Лесосибирск': ['58.2358', '92.4828'], 'Ливны': ['52.4253', '37.6069'],
                      'Липецк': ['52.6031', '39.5708'],
                      'Лиски': ['50.9841', '39.5154'], 'Лобня': ['56.0097', '37.4819'],
                      'Лысьва': ['58.1086', '57.8053'],
                      'Лыткарино': ['55.5827', '37.9052'], 'Люберцы': ['55.6772', '37.8932'],
                      'Магадан': ['59.5638', '150.803'],
                      'Магас': ['43.2226', '44.7726'], 'Магнитогорск': ['53.4186', '59.0472'],
                      'Майкоп': ['44.6078', '40.1058'],
                      'Махачкала': ['42.9764', '47.5024'], 'Междуреченск': ['53.6942', '88.0603'],
                      'Мелеуз': ['52.9647', '55.9328'], 'Миасс': ['55.045', '60.1083'],
                      'Минеральные Воды': ['44.2103', '43.1353'], 'Минусинск': ['53.7103', '91.6875'],
                      'Михайловка': ['50.06', '43.2379'], 'Михайловск': ['45.1283', '42.0256'],
                      'Мичуринск': ['52.8978', '40.4907'], 'Мурманск': ['68.9792', '33.0925'],
                      'Муром': ['55.575', '42.0426'],
                      'Мытищи': ['55.9116', '37.7308'], 'Набережные Челны': ['55.7254', '52.4112'],
                      'Назарово': ['56.0104', '90.4011'], 'Назрань': ['43.226', '44.7732'],
                      'Нальчик': ['43.4981', '43.6189'],
                      'Наро-Фоминск': ['55.3875', '36.7331'], 'Нарьян-Мар': ['67.6387', '53.0037'],
                      'Находка': ['42.8138', '132.873'], 'Невинномысск': ['44.6333', '41.9444'],
                      'Нерюнгри': ['56.6664', '124.638'], 'Нефтекамск': ['56.092', '54.2661'],
                      'Нефтеюганск': ['61.0998', '72.6035'], 'Нижневартовск': ['60.9344', '76.5531'],
                      'Нижнекамск': ['55.6366', '51.8245'], 'Нижний Новгород': ['56.3287', '44.002'],
                      'Нижний Тагил': ['57.9194', '59.965'], 'Ново-Переделкино': ['55.6453', '37.3358'],
                      'Новоалтайск': ['53.3917', '83.9363'], 'Новокузнецк': ['53.7557', '87.1099'],
                      'Новокуйбышевск': ['53.0959', '49.9462'], 'Новомосковск': ['54.0105', '38.2846'],
                      'Новороссийск': ['44.7244', '37.7675'], 'Новосибирск': ['55.0415', '82.9346'],
                      'Новотроицк': ['51.203', '58.3266'], 'Новоуральск': ['57.2439', '60.0839'],
                      'Новочебоксарск': ['56.111', '47.4776'], 'Новочеркасск': ['47.421', '40.0919'],
                      'Новошахтинск': ['47.7604', '39.9333'], 'Новый Уренгой': ['66.0833', '76.6333'],
                      'Ногинск': ['55.8665', '38.4438'], 'Норильск': ['69.3535', '88.2027'],
                      'Ноябрьск': ['63.1931', '75.4373'],
                      'Нягань': ['62.1406', '65.3936'], 'Обнинск': ['55.0968', '36.6101'],
                      'Одинцово': ['55.678', '37.2777'],
                      'Озёрск': ['55.7556', '60.7028'], 'Октябрьский': ['54.4815', '53.471'],
                      'Омск': ['54.9924', '73.3686'],
                      'Орёл': ['52.9651', '36.0785'], 'Оренбург': ['51.7727', '55.0988'],
                      'Орехово-Зуево': ['55.8067', '38.9618'],
                      'Орск': ['51.2049', '58.5668'], 'Отрадный': ['53.376', '51.3452'],
                      'Павлово': ['55.9686', '43.0912'],
                      'Павловский Посад': ['55.7819', '38.6502'], 'Пенза': ['53.2007', '45.0046'],
                      'Первоуральск': ['56.9053', '59.9436'], 'Пермь': ['58.0105', '56.2502'],
                      'Петергоф': ['59.8833', '29.9'],
                      'Петрозаводск': ['61.7849', '34.3469'], 'Петропавловск-Камчатский': ['53.0444', '158.651'],
                      'Подольск': ['55.4242', '37.5547'], 'Полевской': ['56.4422', '60.1878'],
                      'Прокопьевск': ['53.9059', '86.719'], 'Прохладный': ['43.7574', '44.0297'],
                      'Псков': ['57.8136', '28.3496'],
                      'Пушкин': ['59.7142', '30.3964'], 'Пушкино': ['56.0172', '37.8667'],
                      'Пятигорск': ['44.0486', '43.0594'],
                      'Раменское': ['55.5669', '38.2303'], 'Ревда': ['56.801', '59.9303'],
                      'Реутов': ['55.7611', '37.8575'],
                      'Ржев': ['56.2624', '34.3282'], 'Рославль': ['53.9528', '32.8639'],
                      'Россошь': ['50.1983', '39.5673'],
                      'Ростов-на-Дону': ['47.2313', '39.7233'], 'Рубцовск': ['51.5147', '81.2061'],
                      'Рыбинск': ['58.0446', '38.8426'], 'Рязань': ['54.6269', '39.6916'],
                      'Салават': ['53.3837', '55.9077'],
                      'Салехард': ['66.53', '66.6019'], 'Сальск': ['46.4747', '41.5411'],
                      'Самара': ['53.2001', '50.15'],
                      'Санкт-Петербург': ['59.9386', '30.3141'], 'Саранск': ['54.1838', '45.1749'],
                      'Сарапул': ['56.4763', '53.7978'], 'Саратов': ['51.5406', '46.0086'],
                      'Саров': ['54.9358', '43.3235'],
                      'Свободный': ['51.3753', '128.141'], 'Северодвинск': ['64.5635', '39.8302'],
                      'Североморск': ['69.0689', '33.4162'], 'Северск': ['56.6006', '84.8864'],
                      'Сергиев Посад': ['56.3', '38.1333'], 'Серов': ['59.6033', '60.5787'],
                      'Серпухов': ['54.9158', '37.4111'],
                      'Сибай': ['52.7181', '58.6658'], 'Славянск-на-Кубани': ['45.2558', '38.1256'],
                      'Смоленск': ['54.7818', '32.0401'], 'Снежинск': ['56.085', '60.7314'],
                      'Соликамск': ['59.6316', '56.7685'],
                      'Солнечногорск': ['56.1833', '36.9833'], 'Сосновый Бор': ['59.8996', '29.0857'],
                      'Сочи': ['43.5992', '39.7257'], 'Ставрополь': ['45.0428', '41.9734'],
                      'Старый Оскол': ['51.2967', '37.8417'], 'Стерлитамак': ['53.6246', '55.9501'],
                      'Ступино': ['54.9008', '38.0708'], 'Сунжа': ['43.3195', '45.0491'],
                      'Сургут': ['61.25', '73.4167'],
                      'Сызрань': ['53.1585', '48.4681'], 'Сыктывкар': ['61.6764', '50.8099'],
                      'Таганрог': ['47.2362', '38.8969'],
                      'Талнах': ['69.4865', '88.3972'], 'Тамбов': ['52.7317', '41.4433'],
                      'Тверь': ['56.8584', '35.9006'],
                      'Тимашёвск': ['45.6169', '38.9453'], 'Тихвин': ['59.6451', '33.5294'],
                      'Тихорецк': ['45.8547', '40.1253'],
                      'Тобольск': ['58.1981', '68.2546'], 'Тольятти': ['53.5303', '49.3461'],
                      'Томск': ['56.4977', '84.9744'],
                      'Троицк': ['54.0979', '61.5773'], 'Туапсе': ['44.1053', '39.0802'],
                      'Туймазы': ['54.6067', '53.7097'],
                      'Тула': ['54.1961', '37.6182'], 'Тулун': ['54.5636', '100.581'], 'Тюмень': ['57.1522', '65.5272'],
                      'Узловая': ['53.9818', '38.1712'], 'Улан-Удэ': ['51.8272', '107.606'],
                      'Ульяновск': ['54.3282', '48.3866'],
                      'Усолье-Сибирское': ['52.7519', '103.645'], 'Уссурийск': ['43.8029', '131.946'],
                      'Усть-Илимск': ['58.0006', '102.662'], 'Уфа': ['54.7431', '55.9678'],
                      'Ухта': ['63.5671', '53.6835'],
                      'Фрязево': ['55.7332', '38.4646'], 'Фрязино': ['55.9606', '38.0456'],
                      'Хабаровск': ['48.4827', '135.084'],
                      'Ханты-Мансийск': ['61.0042', '69.0019'], 'Хасавюрт': ['43.2509', '46.5877'],
                      'Химки': ['55.897', '37.4297'], 'Чайковский': ['56.7686', '54.1148'],
                      'Чапаевск': ['52.9771', '49.7086'],
                      'Чебоксары': ['56.1322', '47.2519'], 'Челябинск': ['55.154', '61.4291'],
                      'Черёмушки': ['55.6647', '37.5614'], 'Черемхово': ['53.1561', '103.067'],
                      'Череповец': ['59.1333', '37.9'],
                      'Черкесск': ['44.2233', '42.0578'], 'Черногорск': ['53.8236', '91.2842'],
                      'Чехов': ['55.1477', '37.4773'],
                      'Чистополь': ['55.3631', '50.6424'], 'Чита': ['52.0317', '113.501'],
                      'Чусовой': ['58.3013', '57.8131'],
                      'Шадринск': ['56.0852', '63.6335'], 'Шахты': ['47.7091', '40.2144'],
                      'Шуя': ['56.8487', '41.3883'],
                      'Щекино': ['54.0051', '37.5219'], 'Щёлково': ['55.925', '37.9722'],
                      'Эжва': ['61.8128', '50.7283'],
                      'Электросталь': ['55.7896', '38.4467'], 'Элиста': ['46.3078', '44.2558'],
                      'Энгельс': ['51.4839', '46.1053'],
                      'Южно-Сахалинск': ['46.9541', '142.736'], 'Якутск': ['62.0339', '129.733'],
                      'Ярославль': ['57.6299', '39.8737'], 'Ярцево': ['55.0667', '32.6964']}
    # dict_of_cities = dict
    return dict_of_cities