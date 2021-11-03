import cv2
import numpy as np

def Crop(imageNum, imageLength, imageWidth):

    imgname = 'pic/' + ("%04d" % imageNum) + '.bmp'
    img = cv2.imread(imgname)  # input image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # change to gray image

    # Local threshold segmentation, to binary image
    # dst = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,31, 1) #101

    # Global threshold segmentation,  to binary image. (Otsu)
    res, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  # 0,255

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # Morphological denoising
    dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, element)  # Open operation denoising

    contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Contour detection function
    # cv2.drawContours(dst, contours, -1, (120, 0, 0), 2)  # Draw contour

    maxArea = 0
    maxCont = []
    # maxWidth = 0
    # maxHeight = 0
    for cont in contours:
        ares = cv2.contourArea(cont)  # Calculate the area of the enclosing shape
        if ares < 500:  # ignore other contours
            continue
        # print("{}-blob:{}".format(count,ares),end="  ") #area of each shape
        rect = cv2.boundingRect(cont)  # Extract rectangle coordinates
        # cv2.rectangle(img, rect, (0, 0, 255), 1)  # Draw the standard rectangle
        if (ares > maxArea) and (rect[0] > 0) and (rect[0] > 0):
            # maxArea = ares
            maxCont = cont
            # maxWidth = width
            # maxHeight = height

    maxRect = cv2.boundingRect(maxCont)  # Extract rectangle coordinates of the target shape
    # print("image:{} x:{} y:{} width:{} height:{}".format(imageNum, maxRect[0], maxRect[1], round(maxWidth), round(maxHeight)))
    # print("image:{} x:{} y:{} width:{} height:{}".format(imageNum, maxRect[0], maxRect[1], maxRect[2], maxRect[3]))

    # save the crop image
    temp_x = round(maxRect[0] - (imageLength - maxRect[2])/2)
    temp_y = round(maxRect[1] - (imageWidth - maxRect[3])/2)
    img_1 = cv2.imread(imgname)
    crop = img_1[temp_y: temp_y + imageWidth, temp_x: temp_x+imageLength]
    cv2.imwrite("./pic/ROI_0{:02d}0.png".format(imageNum-1), crop)

    # get the X, Y , width and height of the object
    # return maxRect[0], maxRect[1], round(maxWidth), round(maxHeight)
    return maxRect[0], maxRect[1], maxRect[2], maxRect[3]
