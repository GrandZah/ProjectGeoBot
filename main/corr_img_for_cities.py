"""подгон фотографий города под размеры"""

'''изображения идут в порядке
   0   01
   02  03'''

import os
from PIL import Image


def correct_img(user_id, *imgs):
    img_0, img_01, img_02, img_03 = imgs[0], imgs[1], imgs[2], imgs[3]
    x = img_0.size[0] + img_01.size[0] + 3
    if img_0.size[1] >= img_01.size[1]:
        img_01 = img_01.resize((img_01.size[0], img_0.size[1]))
    else:
        img_0 = img_0.resize((img_0.size[0], img_01.size[1]))
    y = img_0.size[1] + max(img_02.size[1], img_03.size[1]) + 3
    if img_02.size[1] >= img_03.size[1]:
        img_03 = img_03.resize((img_01.size[0], img_02.size[1]))
    else:
        img_02 = img_02.resize((img_0.size[0], img_03.size[1]))
    img_03 = img_03.resize((img_01.size[0], img_03.size[1]))
    img_02 = img_02.resize((img_0.size[0], img_02.size[1]))
    img = Image.new('RGB', (x, y), (255, 255, 255))
    img.paste(img_0, (0, 0))
    img.paste(img_01, (img_0.size[0] + 3, 0))
    img.paste(img_02, (0, img_0.size[1] + 3))
    img.paste(img_03, (img_0.size[0] + 3, img_0.size[1] + 3))
    img.save(f'{user_id}.png')
    for i in range(4):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'{user_id}_{i}.png')  # УДАЛЯЕМ ЛИШНИЕ ФАЙЛ (КАРТИНКУ)
        os.remove(path)
