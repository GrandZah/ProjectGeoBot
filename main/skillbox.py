from config import BOT_CONFIG
from config_vk_bot import BOT_CONFIG
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC



def vect():
    x_test = [] # реплики
    y = [] # их классы

    for intent, data in BOT_CONFIG['intents'].items():
        for ex in data['examples']:
            x_test.append(ex)
            y.append(intent)

    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 3))
    X = vectorizer.fit_transform(x_test)

    clf_proba = LogisticRegression().fit(X, y)

    # # неполная выборка данных
    #
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    # clf = LogisticRegression().fit(X_train, y_train)
    # print(clf.score(X_test, y_test))
    #
    # # изменен алгоритм обучения
    #
    # clf = LinearSVC().fit(X_train, y_train)
    # print(clf.score(X_test, y_test))

    clf = LinearSVC().fit(X, y)

    return vectorizer, clf

'''
CountVectorizer:
0.4372594303310239
0.21678321678321677
0.2878787878787879
-----------------
TfidfVectorizer:
0.30600461893764436
0.19813519813519814
0.32400932400932403
-------------------
TfidfVectorizer + args(analyzer='char_wb', ngram_range=(2, 4)):
0.3856812933025404
0.2634032634032634
0.38344988344988346
'''