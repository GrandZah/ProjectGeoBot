import os
import time
from pprint import pprint

from bs4 import BeautifulSoup
from translate import Translator
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

from skillbox import vect
from speak_test import recognize


def main(messages):
    global vectorizer, clf
    try:
        print('Start learning...')
        vectorizer, clf = vect()
        print('Successfull...')
        messages = messages  # Поможет следить за действиями пользователя
        vk_session = vk_api.VkApi(
            token="043d2085f951eae9fbd15cd91916f98dc711cdc6ccf681f5495e60da2f6d5816cdd9a3eb90d3a94065c68")  # Токен ВК ГРУППЫ
        vk = vk_session.get_api()  # Подключаем АПИ
        keyboard = VkKeyboard(one_time=True)  # Добавляем кнопки на которые можно будет нажать
        keyboard.add_button("Да", VkKeyboardColor.PRIMARY)
        keyboard.add_button("Нет", VkKeyboardColor.PRIMARY)

        longpoll = VkBotLongPoll(vk_session, 213029364)  # Подключаем ожидание. В скобках АЙДИ ГРУППЫ

        for event in longpoll.listen():  # ПРОСЛУШИВАЕМ

            if event.type == VkBotEventType.MESSAGE_NEW:  # ЕСЛИ НОВОЕ СООБЩЕНИЕ ТО
                print(messages)
                if (event.obj.message['from_id'] not in messages) or (not messages[event.obj.message['from_id']]['thread']):
                    Thread(target=oop, args=(event, messages, keyboard, vk)).start()
    except Exception as error:
        print(error, '-----', datetime.now())


def oop(event, messages, keyboard, vk):
    try:
        t1 = time.time()
        user = info_user(event.obj.message['from_id'])[0]  # ПОЛУЧАЕМ ИНФОРМАЦИЮ О ПОЛЬЗОВАТЕЛЕ
        print('Новое сообщение:')
        print('Для меня от:', user['first_name'], user['last_name'])
        print('Текст:', event.obj.message['text'])
        # ЗАПУСКАЕМ ОСНОВНОЙ КОД (ДИАЛОГ)
        if event.obj.message['from_id'] in messages and messages[event.obj.message['from_id']]['score'] == 10:
            text = 'Ты прошел игру!\n Поздравляю!'
            messages[event.obj.message['from_id']]['good_bye'] = True
        else:
            t0 = time.time()
            text, *keyboard_city = dialog(messages, event.obj.message['from_id'], user, event.obj.message['text'],
                                          vk)
            print(time.time() - t0, '--- dialog')
        if keyboard_city:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=keyboard_city[0].get_keyboard(),
                             random_id=randint(0, 2 ** 64))
            print(time.time() - t0, '--- time to send messages with picture')
            print(time.time() - t1, '--- alll')
        elif not messages[event.obj.message['from_id']]['good_bye']:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             keyboard=keyboard.get_keyboard(),
                             random_id=randint(0, 2 ** 64))
            print(time.time() - t0, '--- time to send message')
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=randint(0, 2 ** 64))
            try:
                del messages[event.obj.message['from_id']]
            except:
                pass
        try:
            messages[event.obj.message['from_id']]['good_bye'] = False
            messages[event.obj.message['from_id']]['thread'] = False
        except:
            pass
    except Exception as error:
        print(error, datetime.now())


def dialog(messages, user_id, user, user_text, vk):
    global true_city, cities
    if validate(user_text.replace(' ', '')):
        # translator = Translator(to_lang="russian")
        # белиберда отключилась из-за апгрейда переводчика
        try:
            user_text = translate(user_text, "ru")
            # user_text = translator.translate(user_text)
        except:
            return 'Ну и белиберда!)\nКто-то не знает анлгийского, м?',
    user_city = user_text
    user_text = recognize(user_text, vectorizer, clf)
    print(user_text)
    if user_id not in messages:  # ЕСЛИ ЭТО ПЕРВЫЙ СЛУЧАЙ ТО ЭТО
        score = 0
        messages[user_id] = {'score': score, 'dialog': ['Хочешь поиграть?'], 'tr_ci': [], 'hint': False, 'good_bye': False, 'thread': True}
        return f"Привет, {user['first_name']}!\n Хочешь поиграть?",
    elif user_text == 'hint':
        messages[user_id]['hint'] = True
        keyboard_city = VkKeyboard(one_time=True)
        for i in cities:
            keyboard_city.add_button(i, VkKeyboardColor.PRIMARY)
        keyboard_city.add_line()
        keyboard_city.add_button('Хватит', VkKeyboardColor.NEGATIVE)
        return f'Начинается на букву ... хм....  -- {messages[user_id]["tr_ci"][0][0]}\n Заканчивается на букву -- {messages[user_id]["tr_ci"][0][-1]}', keyboard_city
    elif user_text == 'no':  # ЗАВЕРШАЕМ БЕСЕДУ
        messages[user_id]['good_bye'] = True
        return "Ну ладно\nВозвращайся!",
    elif user_text == 'yes' and messages[user_id]['dialog'][-1] != '?':  # НАЧИНАЕМ ИГРУ +
        # ДОБАВИЛ(ну то что ниже на строку) ЧТО ПРОВЕРЯЕМ НА ТО что не ОТВЕт ЛИ это на ВОПРОС
        # (потом мы его удаляем после ответа). Вот это помогает
        # and messages[user_id][-1] == 'Хочешь поиграть?' or messages[user_id][-1] == '?':
        messages[user_id]['dialog'].append('?')  # ДОБАВЛЯЕМ ОПРЕДЕЛЯЮЩИЙ ФАКТОР ИГРЫ
        messages[user_id]['dialog'] = set(messages[user_id]['dialog'])  # ЗАЧЕМ ЭТО ???
        messages[user_id]['dialog'] = list(messages[user_id]['dialog'])  # ЗАЧЕМ ЭТО ???
        messages[user_id]['dialog'].sort(reverse=True)  # ЗАЧЕМ ЭТО ???
        t0 = time.time()
        true_city, name, cities = city_to_dict()  # СОСТАВЛЯЕМ ЗАДАНИЕ
        print(time.time() - t0, '--- time to complete task = city_to(convert) + ok')
        text = f'''Угадай город по {name}: \n 1) {cities[0]} \n 2) {cities[1]} \n 3) {cities[2]} \n 4) {cities[3]} \n Помни! За подсказки баллы не даются!!!'''  # СОСТАВЛЯЕМ ТЕКСТ ДЛЯ ПОЛЬЗОВАТЕЛЯ
        keyboard_city = VkKeyboard(one_time=True)
        if messages[user_id]['tr_ci']:
            messages[user_id]['tr_ci'][0] = true_city
        else:
            messages[user_id]['tr_ci'].append(true_city)
        for i in cities:
            keyboard_city.add_button(i, VkKeyboardColor.PRIMARY)
        keyboard_city.add_line()
        keyboard_city.add_button('Подсказка', VkKeyboardColor.POSITIVE)
        keyboard_city.add_line()
        keyboard_city.add_button('Хватит', VkKeyboardColor.NEGATIVE)  # ФОРМИРУЕМ КНОПКИ ДЛЯ ПОЛЬЗОВАТЕЛЯ
        t0 = time.time()
        send_picture(vk, f"static/img/{messages[user_id]['tr_ci'][0]}_{name}", user_id)  # ОТПРАВЛЯЕМ ФОТОГРАФИЮ
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'static/img/{messages[user_id]["tr_ci"][0]}_{name}.png')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
        os.remove(path)
        print(time.time() - t0, '--- send+open')
        return text, keyboard_city  # ВОЗВРАЩАЕМ текст и значение кнопок
    elif user_text == 'info':
        t0 = time.time()
        txt, href, flag, gerb = text_about(messages[user_id]["tr_ci"][0])
        img_ok(user_id, flag, gerb, messages)
        print(time.time() - t0, '--- time to gerb and info')
        ch = Thread(target=send_picture, args=(vk, user_id, user_id))
        try:
            imgel = Image.open(f'{user_id}_flag.jpg')
            sh = '1'
        except:
            sh = ''
        if sh:
            sh = Thread(target=send_picture, args=(vk, f'{user_id}_flag', user_id))
            sh.start()
            ch.start()
            ch.join()
            sh.join()
        else:
            ch.start()
            ch.join()
        try:
            imgel.close()
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'{user_id}_flag.jpg')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
            os.remove(path)
        except:
            pass
        imh = Image.open(f'{user_id}.png')
        imh.close()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'{user_id}.png')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
        os.remove(path)
        keyboard_city = VkKeyboard(one_time=True)
        keyboard_city.add_button("Да", VkKeyboardColor.PRIMARY)
        keyboard_city.add_button("Нет", VkKeyboardColor.PRIMARY)
        keyboard_city.add_line()
        keyboard_city.add_openlink_button("Еще больше информации!!!", href)
        txt += '\n Продолжим?'
        return txt, keyboard_city
    elif messages[user_id]['dialog'][-1] == '?':  # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВОДИТ ОТВЕТ ТО
        T_F = result(user_city, messages[user_id]['tr_ci'][0], cities)  # СРАВНИВАЕМ ОТВЕТ ПОЛЬЗОВАТЕЛЯ с правильным
        if T_F:
            messages[user_id]['score'] += 1 if not messages[user_id]['hint'] else 0
            del messages[user_id]['dialog'][-1]
            messages[user_id]['hint'] = False  # Удаляем знак вопроса (То есть ответ на вопрос закончился)
            keyboard_city = VkKeyboard(one_time=True)
            keyboard_city.add_button("Да", VkKeyboardColor.PRIMARY)
            keyboard_city.add_button("Нет", VkKeyboardColor.PRIMARY)
            keyboard_city.add_line()
            keyboard_city.add_button('Познакомимся с городом!', VkKeyboardColor.POSITIVE)
            return f"Верно! Молодец\n Твой результат: {messages[user_id]['score']}\n Продолжим?\n Или узнаем город поближе?", keyboard_city # Возвращаем ответ
        else:
            messages[user_id]['score'] -= 1  # Снижаем за ошибку
            del messages[user_id]['dialog'][-1]  # Удаляем знак вопроса (То есть ответ на вопрос закончился)
            messages[user_id]['hint'] = False
            keyboard_city = VkKeyboard(one_time=True)
            keyboard_city.add_button("Да", VkKeyboardColor.PRIMARY)
            keyboard_city.add_button("Нет", VkKeyboardColor.PRIMARY)
            keyboard_city.add_line()
            keyboard_city.add_button('Познакомимся с городом!', VkKeyboardColor.POSITIVE)
            return f"Неверно:(\nПравильный ответ:{messages[user_id]['tr_ci'][0]}\nТвой результат:{messages[user_id]['score']}\n Продолжим?\n Или узнаем что-нибудь новенькое об этом городе?", keyboard_city
    else:
        return user_text,


def send_picture(vk, true_city, peer_id):  # отправка ботом фотографии
    upload = VkUpload(vk)
    t0 = time.time()
    try:
        picture = f'{true_city}.png' # Открываем картинку
        response = upload.photo_messages(picture)[0]
    except:
        picture = f'{true_city}.jpg'
        response = upload.photo_messages(picture)[0]
    print(time.time() - t0, 'open picture')
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    t0 = time.time()
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )  # Отправляем фотку
    print(time.time() - t0, '--- send_picture')

def info_user(id):  # Получаем информацию о пользователе
    vk_session = vk_api.VkApi(
        token="aee5b428df6bfcbf30ff8d564149ccc38d1e7b00bb649583b9d0dea48dea35ef1d81320eb12da492f35a3")
    # ЧЕЙ ТОКЕН ?

    vk = vk_session.get_api()
    response = vk.users.get(user_id=id)
    return response


def result(txt, true, cities):  # функция провкерки корректности ответа
    if txt.isdigit():  # ЕСЛИ ЧЕЛОВЕК ВВЕЛ НОМЕР под которым был город А НЕ СЛОВО
        try:
            return cities[int(txt) - 1] == true
        except:
            return False
    return txt.lower() == true.lower()


def validate(nickname):
    return all(map(lambda c: c in ascii_letters, nickname))




if __name__ == '__main__':
    messages = {}
    main(messages)
