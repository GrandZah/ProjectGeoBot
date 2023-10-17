import random
from pprint import pprint

import nltk
import vk_api
from tqdm import tqdm
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from random import sample, randint, choice
from skillbox import vect
from config_vk_bot import BOT_CONFIG
from datetime import datetime
from fuzzywuzzy import fuzz


def recognize(text, vectorizer, clf):
    txt = text.lower()
    intent = clf.predict(vectorizer.transform([txt]))[0]
    new_intent = ''
    sets = set(BOT_CONFIG['intents'][intent]['examples'])
    for i in sets:
        if len(txt) == 0:
            continue
        dist = nltk.edit_distance(i, txt)
        dist /= len(txt)
        if dist <= 0.50:
            new_intent = intent
            break
    if not new_intent:
        new_intent = choice(BOT_CONFIG['intents']['failure_phrases']['examples'])
    text = str(new_intent)
    return text

# if __name__ == '__main__':
#     recognize()