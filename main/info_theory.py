import sqlite3


def theory(id_user, messages):
    con = sqlite3.connect('1.db3')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM tasks WHERE id == ?""", (messages[id_user]['geography']['id_theory'],)).fetchall()
    result = result[0]
    task_img = result[1]
    task_txt = result[2]
    answer = result[3]
    name_module = cur.execute("""SELECT name FROM modules WHERE id == ?""", (result[4],)).fetchall()
    if result[5]:
        add_info = cur.execute("""SELECT text FROM info WHERE id == ?""", (result[5],)).fetchall()[0][0]
    else:
        add_info = ''
    task_txt, task_img, answer, add_info = if_img([(task_img, 'task_img'), (task_txt, 'task_txt'), (answer, 'answer'), (add_info, 'add_info')], id_user)
    return task_txt, task_img, answer, name_module, add_info, len(cur.execute("""SELECT * FROM tasks""").fetchall())


# проверка на то, что текст - фотка в bytes и сохранение её, если да
def if_img(params, id_user):
    task_img, task_txt, answer, add_info = params[0][0], params[1][0], params[2][0], params[3][0]
    for i in params:
        if isinstance(i[0], bytes):
            with open(f"static/img/{id_user}_{i[1]}.jpg", 'wb') as f:
                f.write(i[0])
                f.close()
            if i[1] == 'task_img':
                task_img = 'correct'
            if i[1] == 'task_txt':
                task_txt = 'correct'
            if i[1] == 'answer':
                answer = 'correct'
            if i[1] == 'add_info':
                add_info = 'correct'
    return task_txt, task_img, answer, add_info
