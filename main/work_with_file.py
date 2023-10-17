def file(messages, id_user):
    with open('id.txt', 'r') as f:
        line = f.read()
        flag_1 = False
        if line:
            flag_1 = True
            q = line.split('\n')
            flag = False
            for i in range(len(q)):
                if str(id_user) in q[i]:
                    flag = True
                    a = q[i].split(' ')
                    a[-1] = str(messages[id_user]['geography']['id_test'])
                    a = ' '.join(a)
                    q[i] = a
            if not flag:
                q.append(f"{id_user} - {messages[id_user]['geography']['id_test']}")
        f.close()
        with open('id.txt', 'w') as f:
            if flag_1:
                f.write('\n'.join(q))
            else:
                f.write(f"{id_user} - {messages[id_user]['geography']['id_test']}")
        f.close()