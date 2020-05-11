from PIL import Image
import os
import cv2
import numpy as np

Image.open("./AnotherKiwi/1/1534849290367911.png").save("./AnotherKiwi/positive/1.bmp")

dir_pos_str = ['./AnotherKiwi/1/', './AnotherKiwi/2/', './AnotherKiwi/3/','./AnotherKiwi/4/']
dir_neg_str = './AnotherKiwi/neg/'

# convert positive and save
for dir in dir_pos_str:
    dir_os = os.fsencode(dir)
    for file in os.listdir(dir_os):
        filename = os.fsdecode(file)
        filename_ori = dir + filename
        target_pos = './AnotherKiwi/positive/'
        filename_bmp = target_pos + filename[:-3] + 'bmp'

        # print(filename_bmp)
        Image.open(filename_ori).save(filename_bmp)

# convert negative and save
dir_os = os.fsencode(dir_neg_str)
for file in os.listdir(dir_os):
    filename = os.fsdecode(file)
    filename_ori = dir_neg_str + filename
    target_pos = './AnotherKiwi/negative/'
    filename_bmp = target_pos + filename[:-3] + 'jpg'

    # print(filename_bmp)
    Image.open(filename_ori).save(filename_bmp)


cv2.waitKey(0)