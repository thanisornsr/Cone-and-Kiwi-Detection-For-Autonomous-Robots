import os
import cv2
import numpy as np

green = np.uint8([[[128,128,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)




#
# directory_in_str = './AnotherKiwi/1/'
# filename = './AnotherKiwi/1/1534849290367911.png'
#
# img = cv2.imread(filename)
#
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
# hsv_cropout4 = cv2.rectangle(hsv,(400,175),(640,290),(0,0,0),-1)
#
# hsv_cropout3 = cv2.rectangle(hsv_cropout4,(0,175),(250,290),(0,0,0),-1)
#
# hsv_cropout2 = cv2.rectangle(hsv_cropout3,(0,290),(640,480),(0,0,0),-1)
# hsv_cropout = cv2.rectangle(hsv_cropout2,(0,0),(640,175),(0,0,0),-1)
#
# best_lower = 0
# best_upper = 0
# best_area = -1
#
# for i in range(0,255):
#     for j in range(i+1,255):
#         area_sum = 0
#         test_lower = i
#         test_upper = j
#         lower_kiwi = np.array([test_lower, 0, 0])
#         upper_kiwi = np.array([test_upper, 255, 255])
#         mask_kiwi = cv2.inRange(hsv_cropout, lower_kiwi, upper_kiwi)
#         contours_kiwi, hierarchy = cv2.findContours(mask_kiwi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         for cnt in contours_kiwi:
#             area_sum = area_sum + cv2.contourArea(cnt)
#         print(area_sum)
#         if area_sum > best_area:
#             print('got it!!!!')
#             best_upper = test_upper
#             best_lower = test_lower
#             best_area = area_sum
#             hsv_best = cv2.drawContours(hsv_cropout,contours_kiwi,0,(0,0,255),3)
#
#
#
# cv2.imshow('HSV',hsv_best)
# print('Result!!!')
# print('-----Best lower----')
# print(best_lower)
# print('-----Best upper----')
# print(best_upper)
# print('----Best area-----')
# print(best_area)
# cv2.waitKey(0)
# cv2.destroyAllWindows()