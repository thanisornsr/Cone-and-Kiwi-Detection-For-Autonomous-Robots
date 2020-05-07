import os
import cv2
import numpy as np
import time
directory_in_str1 = './AnotherKiwi/'
directory1 = os.fsencode(directory_in_str1)
for folder in os.listdir(directory1):
    folder_str = os.fsdecode(folder)
    directory_in_str = directory_in_str1+folder_str+'/'
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename = directory_in_str + filename

        img = cv2.imread(filename)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_cropout2 = cv2.rectangle(hsv, (0, 480 - 160), (640, 480), (0, 0, 0), -1)
        hsv_cropout = cv2.rectangle(hsv_cropout2, (0, 0), (640, 120), (0, 0, 0), -1)

        # Detect blue
        lower_kiwi = np.array([170, 150, 40])
        upper_kiwi = np.array([180, 255, 255])
        # OK for 4
        # lower_kiwi = np.array([120, 200, 200])
        # upper_kiwi = np.array([180, 255, 255])
        mask_kiwi = cv2.inRange(hsv_cropout, lower_kiwi, upper_kiwi)

        contours_kiwi, hierarchy = cv2.findContours(mask_kiwi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img_result = img
        max_area = 1000
        min_area = 390
        # Draw blue
        sum_contour = 0
        for cnt in contours_kiwi:
            img_result = cv2.drawContours(img_result, [cnt], 0, (0, 255, 0), 1)
            sum_contour = sum_contour + cv2.contourArea(cnt)
            # if cv2.contourArea(cnt)>min_area and cv2.contourArea(cnt)<max_area:
            #
            #     x, y, w, h = cv2.boundingRect(cnt)
            #     center_x = round(x+w/2)
            #     center_y = round(y+w/2)
            #     img_result = cv2.circle(img_result, (center_x, center_y), round(max(w/2,h/2))+10, (255,0,0), 4 )
        print(sum_contour)
        if sum_contour > 150:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 420)
            fontScale = 1
            fontColor = (0, 0, 255)
            lineType = 2

            cv2.putText(img, 'KIWI found !!!!',
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
        cv2.imshow('HSV', hsv_cropout)
        cv2.imshow('image', img_result)

        cv2.waitKey(0)

        cv2.destroyAllWindows()

