from CalculateVolume import CalculateVolume
from CapturePictures import CaptureAllImages
from CapturePicturesFromVideo import getImagesFromVideo
from CropWithAdjustment import GetArea
import xlrd
from xlutils.copy import copy
from time import time

def ReadFromResult(loc):
    result = xlrd.open_workbook(loc)
    sheet1 = result.sheet_by_index(0)
    rowCount = sheet1.nrows
    wb = copy(result)
    return rowCount, wb


# check whether two images are the same or not, to test whether the object moved during the capturing process or not.
def isSame(dic, num1, num2):
    X_1, Y_1, width_1, height_1 = GetArea(dic, vintValue, num1, "original")
    print(X_1, Y_1, width_1, height_1)
    X_2, Y_2, width_2, height_2 = GetArea(dic, vintValue, num2, "original")
    print(X_2, Y_2, width_2, height_2)
    if abs(X_1 - X_2 > 1) or abs(Y_1 - Y_2 > 1) or abs(width_1 - width_2 > 1) or abs(height_1 - height_2 > 1):
        print("false")
        return False
    else:
        print("true")
        return True


#
def singleTest(name, dic_pro, dic_cap, imageOrFrame, startRow, save):
    startTime = time()
    print("**** Capturing the images start ***")
    if imageOrFrame == 'video':
        getImagesFromVideo(dic_cap)
        if not isSame(dic_cap, 1, 37):
            getImagesFromVideo(dic_cap)
            if not isSame(dic_cap, 1, 37):
                print('Please replace the seed! Thanks!')
            else:
                print("**** Capturing Images Success! ***")
        else:
            print("**** Capturing Images Success! ***")
    else:
        CaptureAllImages(dic_cap)
        if not isSame(dic_cap, 1, 37):
            CaptureAllImages(dic_cap)
            if not isSame(dic_cap, 1, 37):
                print('Please replace the seed! Thanks!')
            else:
                print("**** Capturing Images Success! ***")
        else:
            print("**** Capturing Images Success! ***")

    print("**** calculating start ***")
    CalculateVolume(name, dic_pro, vintValue, pixPerMMAtZ, imageWidth, imageHeight, sheet1, startRow, save)
    print("Total time: --- %s seconds ---" % (time() - startTime) + "\n")


if __name__ == '__main__':

    path_CaptureImage = '/pic_Captured'
    path_Process = 'pic_processing'
    stored = False  # whether store the results into the excel file
    seedName = '55-lg'

    # set up the parameters
    vintValue = 65
    pixPerMMAtZ = 95 / 3.945
    imageWidth = 200
    imageHeight = 200

    # read an excel file, prepare to store the result into it.
    loc = "./result.xls"
    rowCount, wb = ReadFromResult(loc)
    sheet1 = wb.get_sheet(0)

    # single seed test
    singleTest(seedName, path_Process, path_CaptureImage, 'video', rowCount+1, stored)

