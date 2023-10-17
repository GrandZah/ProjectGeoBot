import sqlite3


def tests(id_user, messages):
    con = sqlite3.connect('1.db3')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM tests WHERE id == ?""", (messages[id_user]['geography']['id_test'],)).fetchall()
    result = result[0]
    task_txt = result[1]
    task_img = result[2]
    if task_img:
        with open(f"static/img/{id_user}_tests.jpg", 'wb') as f:
            f.write(task_img)
            f.close()
    answer = result[3]
    variants = result[4]
    return task_txt, task_img, answer, variants