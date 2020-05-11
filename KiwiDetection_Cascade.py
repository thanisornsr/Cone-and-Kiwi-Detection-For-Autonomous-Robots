import os
import cv2
import time
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 420)
fontScale = 1
fontColor = (0, 0, 255)
lineType = 2



kiwi_cascade = cv2.CascadeClassifier('kiwi.xml')
counter = 0 #to count frame>> 2 frame in row - > found
status = 0 #0 is not found 1 is found
statusFarNear = 0
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
        img_h,img_w, img_c = img.shape
        # we can get some ROI from cone
        # lower bound and upper bound for x

        lw_x = 0.35*img_w
        up_x = 0.65*img_w
        # lower bound and upper bound for y
        lw_y = 0.4*img_h
        up_y = 0.6*img_h
        # this is to detect far/near from y value
        thresholdFarNear = 0.65*img_h
        kiwis = kiwi_cascade.detectMultiScale(img, scaleFactor=1.25 , minNeighbors=1 , minSize=(90,90), maxSize=(220,220) )
        found = len(kiwis)
        #this part make it more robust
        if found == 0:
            counter = 0



        if status == 0:
            if counter > 2:
                status = 1
        else:
            if counter <= 2:
                status = 0

        for (x,y,w,h) in kiwis:
            centerx = x+w/2
            centery = y+h/2
            if centerx<up_x and centerx>lw_x and centery<up_y and centery>lw_y:
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                print((y+h)/img_h)
                print('done')
                if (y+h) >= thresholdFarNear :
                    statusFarNear = 1
                else :
                    statusFarNear = 2

                counter = counter + 1
        if status == 0:
            cv2.putText(img, 'Pedal pos = 1.0//Not found',
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
        else:
            if statusFarNear == 1:
                cv2.putText(img, 'Pedal pos = 0.0//Found NEAR',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
            elif statusFarNear == 2:
                cv2.putText(img, 'Pedal pos = 0.5//Found FAR',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            lineType)

        cv2.imshow('img',img)

        # key = cv2.waitKey(150)
        key = cv2.waitKey(40)
        if key == 27:
            cv2.destroyAllWindows()
            break

