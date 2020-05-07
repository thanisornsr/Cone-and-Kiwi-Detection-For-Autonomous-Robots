import os
import cv2
import numpy as np

directory_in_str = './Cone/'
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filename = directory_in_str + filename

    img = cv2.imread(filename)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_cropout = cv2.rectangle(hsv,(0,0),(1255,300),(0,0,0),-1)

    # Detect blue
    lower_blue = np.array([110,45,45])
    upper_blue = np.array([135,255,255])
    mask_blue = cv2.inRange(hsv_cropout, lower_blue,upper_blue)

    # Detect yellow
    lower_yellow = np.array([18,30,30])
    upper_yellow = np.array([60,255,255])
    mask_yellow = cv2.inRange(hsv_cropout, lower_yellow,upper_yellow)

    contours_blue, hierarchy = cv2.findContours(mask_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, hierarchy = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_result = img
    max_area = 6000
    min_area = 850
    # Draw blue
    for cnt in contours_blue:
        if cv2.contourArea(cnt)>min_area and cv2.contourArea(cnt)<max_area:

            x, y, w, h = cv2.boundingRect(cnt)
            center_x = round(x+w/2)
            center_y = round(y+w/2)
            img_result = cv2.circle(img_result, (center_x, center_y), round(max(w/2,h/2))+10, (255,0,0), 4 )
    # Draw Yellow
    for cnt in contours_yellow:
        # print(cv2.contourArea(cnt))
        # img_result = cv2.drawContours(img_result,[cnt], 0, (0,255,255),3 )


        if cv2.contourArea(cnt)>min_area and cv2.contourArea(cnt)<max_area:

            x, y, w, h = cv2.boundingRect(cnt)
            center_x = round(x+w/2)
            center_y = round(y+w/2)
            img_result = cv2.circle(img_result, (center_x, center_y), round(max(w/2,h/2))+10, (0,255,255), 4 )

    cv2.imshow('HSV',hsv)
    cv2.imshow('image',img_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()