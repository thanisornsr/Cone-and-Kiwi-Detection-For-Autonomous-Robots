import os
import cv2
import numpy as np

dir_bright = './AnotherKiwi/4/1534849454637913.png'
dir_dark = './AnotherKiwi/2/1534849379452440.png'

img_b = cv2.imread(dir_bright)
img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
size_b = img_b.shape
all_pixel_b = size_b[0]*size_b[1]

value_b = sum(sum(img_b))/all_pixel_b
print(value_b)

img_d = cv2.imread(dir_dark)
img_d = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)
size_d = img_d.shape
all_pixel_d = size_d[0]*size_d[1]

value_d = sum(sum(img_d))/all_pixel_d
print(value_d)
# print(img_b)