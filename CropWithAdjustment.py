import cv2
import numpy as np
import math


# get the area of the target (seed) from the side view of image : pic
def GetArea(dic, vintValue, imageNum, imageType):
    if imageType == "original":
        imgname = dic + ("%04d" % imageNum) + '.bmp'
    else:
        # "./pic/ROI_0{:02d}0.png".format(imageNum - 1)
        imgname = dic + 'ROI_0{:02d}0.png'.format(imageNum - 1)
    img = cv2.imread(imgname)  # input image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # change to gray image
    res, dst = cv2.threshold(gray, vintValue, 255, 0)  # 0,255 cv2.THRESH_OTSU
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # Morphological denoising
    dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, element)  # Open operation denoising

    contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)  # Contour detection function
    # cv2.drawContours(dst, contours, -1, (120, 0, 0), 2)  # Draw contour
    maxCont = 0
    for cont in contours:
        area = cv2.contourArea(cont)  # Calculate the area of the enclosing shape
        if area < 1000:  # keep the largest one, which is the target.
            continue
        maxCont = cont
    maxRect = cv2.boundingRect(maxCont)
    X = maxRect[0]
    Y = maxRect[1]
    width = maxRect[2]
    height = maxRect[3]
    return X, Y, width, height


# get the expected width of each image, that is the width when the seed located in the exact turn center
# find the width of the pair opposite images, then calculate the average to get the expected width(the center position)
# the largest one is the length of the target(seed), the smallest one is the width of the target(seed)
def getExpectedValues(dic, vintValue, src):
    expectedWidth = []
    heights = []  # the height of all 36 images.
    imgNum = 1
    while imgNum < 19:  # the first 18 images
        X, Y, width, height = GetArea(dic, vintValue, imgNum, src)
        oppoX, oppoY, oppositeWidth, oppositeHeight = GetArea(dic, vintValue, imgNum + 18, src)
        expectedWidth.append(width / 2 + oppositeWidth / 2)
        # expectedWidth.append(math.ceil(width / 2 + oppositeWidth / 2))
        heights.append(height)
        heights.append(oppositeHeight)
        imgNum += 1
    index = 19
    while index > 1:  # the last 18 images
        expectedWidth.append(expectedWidth[19 - index])
        index -= 1
    # print("expectedWidth: ")
    # print(expectedWidth)
    # print("********** ")
    return expectedWidth, heights


def normalizeImage(dic, vintValue, imageNum, expectedWidth, imageWidth, imageHeight, bottomY):
    imgname = dic + ("%04d" % imageNum) + '.bmp'
    img = cv2.imread(imgname)  # read input image
    X, Y, width, height = GetArea(dic, vintValue, imageNum, "original")
    firstCrop = img[Y: Y + height, X: X + width]  # get the target

    H = firstCrop.shape[0]
    W = firstCrop.shape[1]

    ratio = expectedWidth / width
    newW = math.ceil(W * ratio)
    newH = math.ceil(H * ratio)
    dim = (newW, newH)
    resized = cv2.resize(firstCrop, dim, interpolation=cv2.INTER_AREA)  # resize the target (increase or decrease)

    result = np.zeros([imageHeight, imageWidth, 3], dtype=np.uint8)
    start_Y = math.ceil((imageHeight - newH) / 2)
    start_X = math.ceil((imageWidth - newW) / 2)
    # make the new target in the center of the result
    if bottomY == 0:    # the 1st image.
        result[start_Y: start_Y + newH, start_X: start_X + newW] = resized
    else:
        result[bottomY - newH: bottomY, start_X: start_X + newW] = resized
    # save the image
    cv2.imwrite(dic + "ROI_0{:02d}0.png".format(imageNum - 1), result)

    X, Y, width, height = GetArea(dic, vintValue, imageNum, "roi")
    # print("image:{} x:{} y:{} width:{} height:{}".format(imageNum, X, Y, width, height))
    return start_Y + newH


def CropWithAdjustment(dic, vintValue, imageWidth, imageHeight, expectedWidth):
    # get the stand bottomY position in the image
    bottomY = normalizeImage(dic, vintValue, 1, expectedWidth[0], imageWidth, imageHeight, 0)  # 1/0.
    imgNum = 2
    while imgNum < 37:
        normalizeImage(dic, vintValue, imgNum, expectedWidth[imgNum - 1], imageWidth, imageHeight, bottomY)
        imgNum += 1

#
# def increaseImage(imageNum, X, Y, width, height, expectedWidth, imageWidth, imageHeight):
#     imgname = 'pic/' + ("%04d" % imageNum) + '.bmp'
#     img = cv2.imread(imgname)  # read input image
#     temp_x = math.ceil(X - (imageWidth - width) / 2)
#     temp_y = math.ceil(Y - (imageHeight - height) / 2)
#     #firstCrop = img[temp_y: temp_y + imageHeight, temp_x: temp_x + imageWidth] #get the center part of original image
#     firstCrop = img[0: Y + height, temp_x: temp_x + imageWidth]
#
#     H = firstCrop.shape[0]
#     W = firstCrop.shape[1]
#
#     adjustX = expectedWidth - width  # the pixel of need to increase X
#     ratio = adjustX / width  # the adjust ratio
#     newW = math.ceil(W * (1 + ratio))
#     newH = math.ceil(H * (1 + ratio))
#     dim = (newW, newH)
#     resized = cv2.resize(firstCrop, dim, interpolation=cv2.INTER_AREA)  # resize the firstCrop image (increase)
#     # ########
#     gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # change to gray image
#     # Global threshold segmentation,  to binary image. (Otsu)
#     res, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  # 0,255
#     element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # Morphological denoising
#     dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, element)  # Open operation denoising
#
#     contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL,
#                                            cv2.CHAIN_APPROX_SIMPLE)  # Contour detection function
#     # cv2.drawContours(dst, contours, -1, (120, 0, 0), 2)  # Draw contour
#     maxCont = 0
#     for cont in contours:
#         area = cv2.contourArea(cont)  # Calculate the area of the enclosing shape
#         if area < 500:  # keep the largest one, which is the target.
#             continue
#         maxCont = cont
#     maxRect = cv2.boundingRect(maxCont)
#     Y = maxRect[1]
#     height = maxRect[3]
#
#     # #######
#     # prepare to crop the center of the firstCrop image with the size of imageWidth and imageHeight
#     start_Y = math.ceil((dim[1] - H) / 2)
#     start_X = math.ceil((dim[0] - W) / 2)
#     # secondCrop = resized[start_Y: start_Y + H, start_X: start_X + W]  #get the center part of resized image
#     secondCrop = resized[Y + height - 150: Y + height, start_X: start_X + W]
#
#     cv2.imwrite("./pic/ROI_0{:02d}0.png".format(imageNum - 1), secondCrop)
#
#     X, Y, width, height = GetArea(imageNum, "roi")
#     print("image:{} x:{} y:{} width:{} height:{}".format(imageNum, X, Y, width, height))
#
#
# def decreaseImage(imageNum, X, Y, width, height, expectedWidth, imageWidth, imageHeight):
#     imgname = 'pic/' + ("%04d" % imageNum) + '.bmp'
#     img = cv2.imread(imgname)  # read input image
#     temp_x = math.ceil(X - (imageWidth - width) / 2)
#     temp_y = math.ceil(Y - (imageHeight - height) / 2)
#     # firstCrop = img[temp_y: temp_y + imageHeight, temp_x: temp_x + imageWidth]  #get the center part of original image
#     firstCrop = img[0: Y + height, temp_x: temp_x + imageWidth]
#
#     H = firstCrop.shape[0]
#     W = firstCrop.shape[1]
#
#     adjustX = width - expectedWidth  # the pixel of need to decrease X
#     ratio = adjustX / width  # the adjust ratio
#     newW = math.ceil(W * (1 - ratio))
#     newH = math.ceil(H * (1 - ratio))
#     dim = (newW, newH)
#     resized = cv2.resize(firstCrop, dim, interpolation=cv2.INTER_AREA)  # resize the firstCrop image (decrease)
#
#     # copy the resized image into the template size image by pixels
#     temp = np.zeros([600, 600, 3], dtype=np.uint8)
#     hh, ww, _ = temp.shape
#     startY = math.ceil((hh - dim[1]) / 2)
#     startX = math.ceil((ww - dim[0]) / 2)
#     result = temp.copy()
#     result[startY: startY + dim[1], startX: startX + dim[0]] = resized
#
#     # ########
#     gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # change to gray image
#     # Global threshold segmentation,  to binary image. (Otsu)
#     res, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  # 0,255
#     element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # Morphological denoising
#     dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, element)  # Open operation denoising
#
#     contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL,
#                                            cv2.CHAIN_APPROX_SIMPLE)  # Contour detection function
#     # cv2.drawContours(dst, contours, -1, (120, 0, 0), 2)  # Draw contour
#     maxCont = 0
#     for cont in contours:
#         area = cv2.contourArea(cont)  # Calculate the area of the enclosing shape
#         if area < 500:  # keep the largest one, which is the target.
#             continue
#         maxCont = cont
#     maxRect = cv2.boundingRect(maxCont)
#     Y = maxRect[1]
#     height = maxRect[3]
#     # #######
#
#     # prepare to crop the center of the result image with the size of imageWidth and imageHeight
#     start_Y = math.ceil((hh - H) / 2)
#     start_X = math.ceil((ww - W) / 2)
#     # secondCrop = result[start_Y: start_Y + H, start_X: start_X + W]  # get the center part of resized image
#     secondCrop = result[Y + height - 150: Y + height, start_X: start_X + W]
#
#     cv2.imwrite("./pic/ROI_0{:02d}0.png".format(imageNum - 1), secondCrop)
#
#     print("decrease")
#     X, Y, width, height = GetArea(imageNum, "roi")
#     print("image:{} x:{} y:{} width:{} height:{}".format(imageNum, X, Y, width, height))
