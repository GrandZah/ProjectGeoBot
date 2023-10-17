'''
крч тут я хочу сделать диалог по-нормальному
07.06 21:11 - создан файл
'''

import os
import time
from pprint import pprint

from PIL import Image
from string import ascii_letters
from random import sample, randint, choice
import requests
from mtranslate import translate

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from threading import Thread
from city_to_dict import city_to_dict
from info_city import img_ok, text_about
from datetime import datetime

print(f'[log] {datetime.now().strftime("%H:%M:%S")} Start learning...')
from skillbox import vect
from speak_test import recognize

print(f'[log] {datetime.now().strftime("%H:%M:%S")} Done')

from config_vk_bot import BOT_CONFIG
from info_theory import theory
from info_test import tests

from work_with_file import file


def main(messages):
    global vectorizer, clf, GAMES, GAME, SCORES

    # функции для всех игр
    GAMES = {'cities': cities, 'geography': geography_keyboard}
    GAME = ['Города', 'География']
    SCORES = {'cities_': 10, 'geography_theory': 32, 'geography_test': 20}

    # обучение ии
    vectorizer, clf = vect()

    # подключение API
    vk_session = vk_api.VkApi(
        token="TOKEN_GROUP")
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, 212743934)

    # прослушиваем новые сообщения
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if (event.obj.message['from_id'] not in messages) or (not messages[event.obj.message['from_id']]['thread']):
                Thread(target=response,
                       args=(event.obj.message['from_id'], messages, vk, event.obj.message['text'])).start()


def response(id_user, messages, vk, user_text):
    if id_user not in messages:  # первый ли раз кожаный написал
        # текст для знакомства (дайвинчик)
        name = user_name(id_user)
        text = choice(BOT_CONFIG['intents']['hello']['responses']) + ', ' + name
        text += '\nХочешь поиграть?'

        # клава (кока)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
        keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)

        # Здороваемся
        vk.messages.send(user_id=id_user,
                         message=text,
                         keyboard=keyboard.get_keyboard(),
                         random_id=randint(0, 2 ** 64))

        # вносим в тетрадь смерти
        messages[id_user] = {
            'cities': {'score': 0, 'gaming': False, 'true_city': '', 'arr_city': [], 'hint': False, 'asking': '',
                       'game': ''},
            'geography': {'id_theory': 1, 'gaming': False, 'game': '', 'add_info': '', 'answer_theory': '',
                          'id_test': 1,
                          'score': 0, 'answer_test': '', 'about_answer': {'correct': 0, 'not_counted': 0, 'wrong': 0},
                          'test_var': ''},
            'thread': True,
            'bye': False}
    else:
        # запуск разговора
        messages[id_user]['thread'] = True
        text, keyboard = dialog(id_user, messages, vk, user_text)
        if keyboard:
            vk.messages.send(user_id=id_user,
                             message=text,
                             keyboard=keyboard.get_keyboard(),
                             random_id=randint(0, 2 ** 64))
        else:  # только если попрощались да поцеловались
            vk.messages.send(user_id=id_user,
                             message=text,
                             random_id=randint(0, 2 ** 64))
            file(messages, id_user)
            del messages[id_user]
    try:
        messages[id_user]['thread'] = False
    except:
        pass


def dialog(id_user, messages, vk, user_text):
    if validate(user_text.replace(' ', '')):
        user_text = translate(user_text, "ru")

    # распознаем речь
    user_txt = user_text
    user_text = recognize(user_text.lower(), vectorizer, clf)

    game = gaming(id_user, messages)
    if user_text == 'bye':
        return choice(BOT_CONFIG['intents']['bye']['responses']), []
    elif not game:
        txt, keyboard = no_gaming(user_text, vk, user_txt, id_user, messages)
        return txt, keyboard
    elif game == 'cities':
        txt, keyboard = cities(user_text, vk, user_txt, id_user, messages)
        return txt, keyboard
    elif game == 'geography':
        txt, keyboard = geography(user_text, vk, user_txt, id_user, messages)
        return txt, keyboard


# имя пользователя
def user_name(id_user):
    vk_session = vk_api.VkApi(
        token="ACCESS_TOKEN_VK_COM")
    vk = vk_session.get_api()
    response = vk.users.get(user_id=id_user)
    return response[0]['first_name']


# играет ли чувак во что-нибудь
def gaming(id_user, messages):
    game = ''
    for games, info_games in messages[id_user].items():
        if type(info_games) == type({}):
            if info_games['gaming']:
                game = games
                break
    return game


# функция для неиграбельного процесса
def no_gaming(user_text, vk, user_txt, id_user, messages):
    if user_text == 'yes':
        txt = 'Выбирай:'
        keyboard = VkKeyboard(one_time=True)
        for i in range(len(GAMES.keys())):
            keyboard.add_button(GAME[i], VkKeyboardColor.PRIMARY)
            txt += f'\n {i + 1}) {GAME[i]}'
        return txt, keyboard
    elif user_text == 'no':
        return choice(BOT_CONFIG['intents']['bye']['responses']), []
    else:
        try:
            ind = list(GAMES.keys())[GAME.index(user_txt.lower().capitalize())]
            text, keyboard = GAMES[ind](user_text, vk, user_txt, id_user, messages)
            return text, keyboard
        except:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)

            txt = choice(BOT_CONFIG['intents']['failure_phrases']['examples'])
            send_text(vk, txt, id_user)

            txt = 'Продолжим играть?'
            return txt, keyboard


# функция для игры в города
def cities(user_text, vk, user_txt, id_user, messages):
    if user_txt == 'Города' and not messages[id_user]['cities']['gaming']:  # запуск функции в первый раз
        messages[id_user]['cities']['gaming'] = True
        messages[id_user]['cities']['asking'] = '?'
        true_city, name, cities = city_to_dict()
        text = f'''Угадай город по {name}: \n 1) {cities[0]} \n 2) {cities[1]} \n 3) {cities[2]} \n 4) {cities[3]} \n Помни! За подсказки баллы не даются!!!'''
        keyboard_city = VkKeyboard(one_time=True)
        messages[id_user]['cities']['true_city'] = true_city
        messages[id_user]['cities']['arr_city'] = cities
        for i in cities:
            keyboard_city.add_button(i, VkKeyboardColor.PRIMARY)
        keyboard_city.add_line()
        keyboard_city.add_button('Подсказка', VkKeyboardColor.POSITIVE)
        keyboard_city.add_line()
        keyboard_city.add_button('Хватит', VkKeyboardColor.NEGATIVE)
        send_picture(vk, f"static/img/{messages[id_user]['cities']['true_city']}_{name}", id_user)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f"static/img/{messages[id_user]['cities']['true_city']}_{name}.png")
        os.remove(path)

        return text, keyboard_city
    else:
        if user_text == 'no':
            txt = answers(user_text, vk, user_txt, id_user, messages)
            send_text(vk, txt, id_user)

            txt = 'Продолжим играть?'
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Да', VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Нет', VkKeyboardColor.PRIMARY)
            messages[id_user]['cities']['asking'] = ''
            messages[id_user]['cities']['gaming'] = False
            messages[id_user]['cities']['score'] = 0
            return txt, keyboard
        elif user_text == 'hint' and messages[id_user]['cities']['asking']:
            messages[id_user]['cities']['hint'] = True
            keyboard_city = VkKeyboard(one_time=True)
            for i in messages[id_user]['cities']['arr_city']:
                keyboard_city.add_button(i, VkKeyboardColor.PRIMARY)
            keyboard_city.add_line()
            keyboard_city.add_button('Хватит', VkKeyboardColor.NEGATIVE)
            text = hint(messages, id_user)
            return text, keyboard_city
        elif messages[id_user]['cities']['asking']:
            win_or_lose = result(user_txt, messages[id_user]['cities']['true_city'],
                                 messages[id_user]['cities']['arr_city'])
            if win_or_lose:
                messages[id_user]['cities']['score'] += 1 if not messages[id_user]['cities']['hint'] else 0
                messages[id_user]['cities']['asking'] = ''
                messages[id_user]['cities']['hint'] = False
                keyboard_city = VkKeyboard(one_time=True)
                keyboard_city.add_button("Да", VkKeyboardColor.PRIMARY)
                keyboard_city.add_button("Нет", VkKeyboardColor.PRIMARY)
                keyboard_city.add_line()
                keyboard_city.add_button('Познакомимся с городом!', VkKeyboardColor.POSITIVE)
                return f"Верно! Молодец\n Твой результат: {messages[id_user]['cities']['score']}\n Продолжим?\n Или узнаем город поближе?", keyboard_city  # Возвращаем ответ
            else:
                messages[id_user]['cities']['score'] -= 1  # Снижаем за ошибку
                messages[id_user]['cities']['asking'] = ''  # Удаляем знак вопроса (То есть ответ на вопрос закончился)
                messages[id_user]['cities']['hint'] = False
                keyboard_city = VkKeyboard(one_time=True)
                keyboard_city.add_button("Да", VkKeyboardColor.PRIMARY)
                keyboard_city.add_button("Нет", VkKeyboardColor.PRIMARY)
                keyboard_city.add_line()
                keyboard_city.add_button('Познакомимся с городом!', VkKeyboardColor.POSITIVE)

                txt = f"Правильный ответ: {messages[id_user]['cities']['true_city']}\n Твой результат: {messages[id_user]['cities']['score']}\n Продолжим?\n Или узнаем что-нибудь новенькое об этом городе?"
                flag_for_user = False
                for i in messages[id_user]['cities']['arr_city']:
                    if user_txt.lower().capitalize() == i.lower().capitalize():
                        flag_for_user = True
                if not flag_for_user:
                    txt = "Может быть ты начнешь использовать клаву?\n " + txt
                else:
                    txt = "Неверно:(\n " + txt
                return txt, keyboard_city
        elif user_text == 'info' and not messages[id_user]['cities']['asking']:
            txt, href, flag, gerb = text_about(messages[id_user]['cities']['true_city'])
            img_ok(id_user, flag, gerb, messages)
            ch = Thread(target=send_picture, args=(vk, id_user, id_user))
            ch.start()
            ch.join()
            imh = Image.open(f'{id_user}.png')
            imh.close()
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'{id_user}.png')
            os.remove(path)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_openlink_button("Еще больше информации!!!", href)
            txt += '\nПродолжим?'
            return txt, keyboard
        elif user_text == 'yes' and not messages[id_user]['cities']['asking']:
            messages[id_user]['cities']['asking'] = '?'
            true_city, name, cities = city_to_dict()
            text = f'''Угадай город по {name}: \n 1) {cities[0]} \n 2) {cities[1]} \n 3) {cities[2]} \n 4) {cities[3]} \n Помни! За подсказки баллы не даются!!!'''
            keyboard_city = VkKeyboard(one_time=True)
            messages[id_user]["cities"]["true_city"] = true_city
            messages[id_user]['cities']['arr_city'] = cities
            for i in cities:
                keyboard_city.add_button(i, VkKeyboardColor.PRIMARY)
            keyboard_city.add_line()
            keyboard_city.add_button('Подсказка', VkKeyboardColor.POSITIVE)
            keyboard_city.add_line()
            keyboard_city.add_button('Хватит', VkKeyboardColor.NEGATIVE)
            send_picture(vk, f'static/img/{messages[id_user]["cities"]["true_city"]}_{name}', id_user)

            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'static/img/{messages[id_user]["cities"]["true_city"]}_{name}.png')
            os.remove(path)

            return text, keyboard_city
        else:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Познакомимся с городом!', VkKeyboardColor.POSITIVE)
            return choice(BOT_CONFIG['intents']['failure_phrases']['examples']), keyboard


# отправка ботом фотографии
def send_picture(vk, true_city, peer_id):
    upload = VkUpload(vk)
    try:
        picture = f'{true_city}.png'
        response = upload.photo_messages(picture)[0]
    except:
        picture = f'{true_city}.jpg'
        response = upload.photo_messages(picture)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment)


# для нужды отправить сообщение, если связать с основной отправкой не получается
def send_text(vk, user_txt, id_user):
    vk.messages.send(user_id=id_user,
                     message=user_txt,
                     random_id=randint(0, 2 ** 64))


# проверка на англ
def validate(nickname):
    return all(map(lambda c: c in ascii_letters, nickname))


# функция проверки корректности ответа
def result(txt, true, cities):
    if txt.isdigit():
        try:
            return cities[int(txt) - 1] == true
        except:
            return False
    return txt.lower() == true.lower()


# функция подбора подсказки
def hint(messages, user_id):
    city = messages[user_id]['cities']['true_city']
    cities = messages[user_id]['cities']['arr_city']
    for i in cities:
        if i[0] == city[0] and i[-1] == city[-1]:
            return f"Начинается на букву ... хм....  -- {city[0]}\n Заканчивается на букву -- {city[-1]}"
        elif i[0] == city[0]:
            return f"Начинается на букву ... хм....  -- {city[0]}"
        elif i[-1] == city[-1]:
            return f"Заканчивается на букву .. хм....  -- {city[-1]}"
        elif len(i) == len(city):
            return f"Этот город состоит из {len(city)} букв"
        else:
            return f"Начинается на букву ... хм....  -- {city[0]}\n Заканчивается на букву -- {city[-1]}"


# функция для вывода итогового результата
def answers(user_text, vk, user_txt, id_user, messages):
    for name, params in messages[id_user].items():
        if params['gaming']:
            if messages[id_user][name]['score'] < 0:
                return f"Твой результат ({messages[id_user][name]['score']}) оставляет желать лучшего \nТренируйся!"
            else:
                per = messages[id_user][name]['score'] / SCORES[name + '_' + params['game']] * 100
                return f"Твой итоговый счет: {messages[id_user][name]['score']} - это все лишь {per}% от того, что ты можешь \n Ты потерял хватку"


# функция для выбора части игры в географию
def geography_keyboard(user_text, vk, user_txt, id_user, messages):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Тестовая часть', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Теоретическая часть', VkKeyboardColor.PRIMARY)
    text = 'Выбирай:\n 1. Тестовая часть\n 2. Теоретическая часть'
    messages[id_user]['geography']['gaming'] = True
    return text, keyboard


# функция для самой игры
def geography(user_text, vk, user_txt, id_user, messages):
    if user_text == 'no':
        if messages[id_user]['geography']['game'] == 'test':
            txt = answers(user_text, vk, user_txt, id_user, messages)
            send_text(vk, txt, id_user)

        txt = 'Продолжим играть?'
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Да', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Нет', VkKeyboardColor.PRIMARY)
        messages[id_user]['geography']['game'] = ''
        messages[id_user]['geography']['gaming'] = False
        messages[id_user]['geography']['score'] = 0
        return txt, keyboard
    elif messages[id_user]['geography']['game'] == 'test':
        answer_test = False
        if user_txt not in 'АБВГ' and user_txt.lower() not in messages[id_user]['geography']['test_var'].lower():
            txt = f'Нужно выбирать из предложенных вариантов, а не умничать\nТвой счёт:{messages[id_user]["geography"]["score"]}'
            messages[id_user]["geography"]["about_answer"]["not_counted"] += 1
        elif corr_answer_geo(user_txt, vk, id_user, messages):
            messages[id_user]["geography"]["score"] += 1
            txt = f'Верно) Умница\nТвой счёт: {messages[id_user]["geography"]["score"]}'
            messages[id_user]["geography"]["about_answer"]["correct"] += 1
        else:
            messages[id_user]["geography"]["about_answer"]["wrong"] += 1
            messages[id_user]["geography"]["score"] -= 1
            txt = f'Неверно(  Тренируйся\nТвой счёт: {messages[id_user]["geography"]["score"]}'
            answer_test = True
        send_text(vk, txt, id_user)
        if answer_test:
            txt = f'Павильный ответ: {messages[id_user]["geography"]["answer_test"]}'
            send_text(vk, txt, id_user)
        if messages[id_user]["geography"]["id_test"] == 20:
            txt = f'ИНФО о прохождении:\n -Правильных ответов: {messages[id_user]["geography"]["about_answer"]["correct"]}\n -Незасчитанных: {messages[id_user]["geography"]["about_answer"]["not_counted"]}\n -Неправильных: {messages[id_user]["geography"]["about_answer"]["wrong"]}'
            send_text(vk, txt, id_user)

            txt = 'Продолжим играть?'
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Да', VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Нет', VkKeyboardColor.PRIMARY)
            messages[id_user]['geography']['game'] = ''
            messages[id_user]['geography']['gaming'] = False

            messages[id_user]["geography"]["about_answer"]["not_counted"] = 0
            messages[id_user]["geography"]["about_answer"]["correct"] = 0
            messages[id_user]["geography"]["about_answer"]["wrong"] = 0
            return txt, keyboard
        messages[id_user]["geography"]["id_test"] += 1
        txt, keyboard = test_geo(vk, id_user, messages)
        return txt, keyboard
    elif messages[id_user]['geography']['game'] == 'theory':
        if user_txt == 'Далее' and messages[id_user]['geography']['id_theory'] != 32:
            messages[id_user]['geography']['id_theory'] += 1
            txt, keyboard = theory_geo(vk, id_user, messages)
            return txt, keyboard
        elif user_txt == 'Назад' and messages[id_user]['geography']['id_theory'] != 1:
            messages[id_user]['geography']['id_theory'] -= 1
            txt, keyboard = theory_geo(vk, id_user, messages)
            return txt, keyboard
        elif user_txt == 'Ответ':
            answer = messages[id_user]['geography']['answer_theory']

            keyboard = VkKeyboard(one_time=True)
            if messages[id_user]['geography']['id_theory'] != 32:
                keyboard.add_button('Далее', VkKeyboardColor.PRIMARY)
            if messages[id_user]['geography']['id_theory'] != 1:
                keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            if messages[id_user]['geography']['add_info'] != '2' and messages[id_user]['geography']['add_info']:
                keyboard.add_button('Доп инфа', VkKeyboardColor.POSITIVE)
                keyboard.add_line()
            keyboard.add_button('Хватит', VkKeyboardColor.NEGATIVE)

            if messages[id_user]['geography']['answer_theory'] != '2':
                messages[id_user]['geography']['answer_theory'] = '2'
                if answer == 'correct':
                    send_picture(vk, f"static/img/{id_user}_answer", id_user)

                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        f"static/img/{id_user}_answer.jpg")
                    os.remove(path)

                    return 'Смотри фотку', keyboard
                return answer, keyboard
            return 'Ответ уже вывели', keyboard
        elif user_txt == 'Доп инфа':
            keyboard = VkKeyboard(one_time=True)
            if messages[id_user]['geography']['id_theory'] != 32:
                keyboard.add_button('Далее', VkKeyboardColor.PRIMARY)
            if messages[id_user]['geography']['id_theory'] != 1:
                keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            if messages[id_user]['geography']['answer_theory'] != '2':
                keyboard.add_button('Ответ', VkKeyboardColor.POSITIVE)
                keyboard.add_line()
            keyboard.add_button('Хватит', VkKeyboardColor.NEGATIVE)

            add_info = messages[id_user]['geography']['add_info']
            if messages[id_user]['geography']['add_info'] != '2':
                messages[id_user]['geography']['add_info'] = '2'
                if not add_info:
                    return 'Информация отсутствует...', keyboard
                elif add_info == 'correct':
                    send_picture(vk, f"static/img/{id_user}_add_info", id_user)

                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        f"static/img/{id_user}_add_info.jpg")
                    os.remove(path)

                    return 'Смотри фотку', keyboard
                return add_info, keyboard
            return 'Инфу уже вывели', keyboard
        else:
            keyboard = VkKeyboard(one_time=True)
            if messages[id_user]['geography']['id_theory'] != 32:
                keyboard.add_button('Далее', VkKeyboardColor.PRIMARY)
            if messages[id_user]['geography']['id_theory'] != 1:
                keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Ответ', VkKeyboardColor.POSITIVE)
            if messages[id_user]['geography']['add_info']:
                keyboard.add_button('Доп инфа', VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('Хватит', VkKeyboardColor.NEGATIVE)
            return "Не пытайся меня сломать\nИспользуй клавиатуру", keyboard

    elif user_txt == 'Тестовая часть':
        messages[id_user]['geography']['game'] = 'test'
        txt, keyboard = test_geo(vk, id_user, messages)
        return txt, keyboard
    elif user_txt == 'Теоретическая часть':
        messages[id_user]['geography']['game'] = 'theory'
        txt, keyboard = theory_geo(vk, id_user, messages)
        return txt, keyboard
    else:
        send_text(vk, choice(BOT_CONFIG['intents']['failure_phrases']['examples']), id_user)
        txt, keyboard = geography_keyboard(user_text, vk, user_txt, id_user, messages)
        return txt, keyboard


# функция для тестовой части
def test_geo(vk, id_user, messages):
    task_txt, task_img, answer, variants = tests(id_user, messages)
    send_text(vk, task_txt, id_user)
    if task_img:
        send_picture(vk, f"static\img\{id_user}_tests", id_user)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'static/img/{id_user}_tests.jpg')
        os.remove(path)
    messages[id_user]['geography']['answer_test'] = answer
    messages[id_user]['geography']['test_var'] = variants

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('А', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Б', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('В', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Г', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Хватит', VkKeyboardColor.NEGATIVE)

    return variants, keyboard


# функция для теоретической части
def theory_geo(vk, id_user, messages):
    task_txt, task_img, answer, name_module, add_info, length = theory(id_user, messages)
    if task_txt == task_img:
        q = Thread(target=send_picture, args=(vk, f"static\img\{id_user}_task_txt", id_user))
        j = Thread(target=send_picture, args=(vk, f"static\img\{id_user}_task_img", id_user))
        q.start()
        j.start()
        q.join()
        j.join()

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'static/img/{id_user}_task_img.jpg')
        os.remove(path)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'static/img/{id_user}_task_txt.jpg')
        os.remove(path)

        txt = 'Cмотри фотки'
    else:
        txt = task_txt
        if task_img:
            send_picture(vk, f"static\img\{id_user}_task_img", id_user)

            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'static/img/{id_user}_task_img.jpg')
            os.remove(path)

    messages[id_user]['geography']['answer_theory'] = answer
    messages[id_user]['geography']['add_info'] = add_info

    keyboard = VkKeyboard(one_time=True)
    if messages[id_user]['geography']['id_theory'] != length:
        keyboard.add_button('Далее', VkKeyboardColor.PRIMARY)
    if messages[id_user]['geography']['id_theory'] != 1:
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Ответ', VkKeyboardColor.POSITIVE)
    if add_info:
        keyboard.add_button('Доп инфа', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Хватит', VkKeyboardColor.NEGATIVE)

    return txt, keyboard


# проверка для теста по географии
def corr_answer_geo(user_txt, vk, id_user, messages):
    var = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3}
    true_answer = messages[id_user]['geography']['answer_test']
    variants = messages[id_user]['geography']['test_var'].split('\n')
    if len(user_txt) == 1:
        answer = user_txt.lower() == true_answer.lower()
    else:
        true_var = variants[var[true_answer]]
        answer = user_txt.lower() == true_var.lower() or user_txt.lower() in true_var.lower()
    return answer


if __name__ == '__main__':
    messages = {}
    main(messages)
