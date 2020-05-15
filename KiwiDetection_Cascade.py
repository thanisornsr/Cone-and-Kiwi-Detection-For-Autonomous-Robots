

#This is to import library
import os #This is just to read the file directory
import cv2 #The OpenCV
import numpy as np #Numpy for handle matrix not used yet.



#This is just to show of text showing on the screen
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 420)
fontScale = 1
fontColorNear = (0, 0, 255)
fontColorFar = (255, 0, 0)
fontColorNotFound = (0,255,0)
lineType = 2


# Load the xml file
kiwi_cascade = cv2.CascadeClassifier('kiwi.xml')
# The counter is used to count the condition that if we detect 2 kiwi in rows >> we say that we found kiwi
counter = 0
# To get the status 0>> is not found 1>> is found
status = 0 

# If found this will be update that it's near or it is far.
statusFarNear = 0

# This is just a directory of image>> I try to reach every image in the folder AnotherKiwi
directory_in_str1 = './AnotherKiwi/'
directory1 = os.fsencode(directory_in_str1)
for folder in os.listdir(directory1):

    #This is the same as previous. in AnotherKiwi have 1 2 3 4 neg >> I try to reach all of that
    folder_str = os.fsdecode(folder)
    directory_in_str = directory_in_str1+folder_str+'/'
    directory = os.fsencode(directory_in_str)

    firstFound = 0
    upper_brightness = 255
    lower_brightness = 40
    lower_kiwi1 = np.array([160, 100, lower_brightness])
    upper_kiwi1 = np.array([190, 255, upper_brightness])

    lower_kiwi2 = np.array([0, 0, 0])
    upper_kiwi2 = np.array([30, 30, 50])

    min_area = 500

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename = directory_in_str + filename
        #In this step we have file name. In the .rec version we can skip to this directly
        # Simply read the image
        img = cv2.imread(filename)
        # get the image size
        img_h,img_w, img_c = img.shape
        
        # These parameters are for set the Region of Interest (The region that Kiwi should be at)
        # lower bound and upper bound for center x
        lw_x = 0.3*img_w
        up_x = 0.7*img_w
        # lower bound and upper bound for center y
        lw_y = 0.4*img_h
        up_y = 0.6*img_h
        # this is the threshold we use to decide if it near or far
        thresholdFarNear = int(round(0.55*img_h))
        thresholdWidth = 180
        print(thresholdFarNear)


        #This is OpenCV command to do the detection using cascade
        kiwis = kiwi_cascade.detectMultiScale(img, scaleFactor=1.25 , minNeighbors=1 , minSize=(90,90), maxSize=(220,220) )

        biggestArea = 0
        for (x,y,w,h) in kiwis:
            currentArea = w*h
            if currentArea > biggestArea:
                biggestArea = currentArea
        gotOne = 0

        #For every detection we extract x,y (the top left position) and width, height
        for (x,y,w,h) in kiwis:
            detectedArea = w*h
            if detectedArea == biggestArea:

                # Calculate the center of detected object
                centerx = int(round(x+w/2))
                centery = int(round(y+h/2))





                # Here we check if the object detected is in the region of interest (Avoid false detection)
                if centerx<up_x and centerx>lw_x and centery<up_y and centery>lw_y and gotOne == 0:
                    gotOne = 1

                    scaleROI = 0.15
                    scaleUpROI = 1 + scaleROI
                    scaleDownROI = 1 - scaleROI
                    yStartToCrop = int(round(y*1.05))
                    yEndToCrop = int(round((y+h)*0.95))
                    # yStartToCrop = y
                    # yEndToCrop = y + h
                    xStartToCrop = int(round(x * scaleDownROI))
                    xEndToCrop = int(round((x + w) * scaleUpROI))

                    kiwiROI = img[yStartToCrop:yEndToCrop, xStartToCrop:xEndToCrop]
                    kiwiROIHSV = cv2.cvtColor(kiwiROI, cv2.COLOR_BGR2HSV)

                    # Then we draw the rectangle around it.
                    img = cv2.rectangle(img,(xStartToCrop,yStartToCrop),(xEndToCrop,yEndToCrop),(0,0,255),2)
                    img = cv2.circle(img, (centerx,centery), 2, (0,0,255), thickness = 2)
                    # Nothing here, I just print to see the value myself

                    mask_kiwi1 = cv2.inRange(kiwiROIHSV, lower_kiwi1, upper_kiwi1)
                    mask_kiwi2 = cv2.inRange(kiwiROIHSV, lower_kiwi2, upper_kiwi2)
                    mask_kiwi = cv2.bitwise_or(mask_kiwi1, mask_kiwi2)
                    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
                    mask_kiwi = cv2.morphologyEx(mask_kiwi,cv2.MORPH_CLOSE, rect_kernel)
                    contours_kiwi, hierarchy = cv2.findContours(mask_kiwi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    print("This is new")
                    maxContour = 0
                    # img = cv2.line(img, (0,thresholdFarNear),(img_w,thresholdFarNear),(0,0,255),3)
                    for cnt in contours_kiwi:
                        if cv2.contourArea(cnt) > maxContour:
                            maxContour = cv2.contourArea(cnt)
                    detectedWidth = 0
                    for cnt in contours_kiwi:
                        if cv2.contourArea(cnt) == maxContour:
                            xc, yc, wc, hc = cv2.boundingRect(cnt)
                            # if cv2.contourArea(cnt) > min_area:
                            kiwiROIHSV = cv2.drawContours(kiwiROIHSV, [cnt], 0, (0, 0, 255), 2)
                            detectedWidth = wc
                            print('The width')
                            print(wc)





                    # Check the bottom of detected object. If it is higher than threshold, it is far.
                    if y+h >= thresholdFarNear and detectedWidth >= thresholdWidth:
                        # 1: Near
                        statusFarNear = 1
                    else :
                        # 2: Far
                        statusFarNear = 2
                    # Plus counter
                    counter = counter + 1

                    # If nothing found, we reset counter


                    # if it is not found yet
                    if status == 0:
                        # If this is the second detection in row, we will define as found!
                        if counter > 2:
                            # Set status as found.
                            status = 1
                    else:
                        # If this is not 2 detection in rows, it is still not found.
                        if counter <= 2:
                            status = 0

        if len(kiwis) == 0:
            status = 0

        # In this part I just put the text in the image >> 3 cases: not found far near.
        if status == 0:
            cv2.putText(img, 'Pedal pos = 1.00//Not found',
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColorNotFound,
                        lineType)
        else:
            if statusFarNear == 1:
                cv2.putText(img, 'Pedal pos = 0.15//Found NEAR',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColorNear,
                            lineType)
            elif statusFarNear == 2:
                cv2.putText(img, 'Pedal pos = 0.65//Found FAR',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColorFar,
                            lineType)
        # Simply show image
        cv2.imshow('img',img)
        # if gotOne :
        #     cv2.imshow('imgCrop',kiwiROIHSV)
        #     cv2.imshow('Inrange',mask_kiwi)

        # Wait before load next image
        key = cv2.waitKey(120)
        if key == 27:
            cv2.destroyAllWindows()
            break

