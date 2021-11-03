from CalculateVolume import CalculateVolume
from CapturePictures import CaptureAllImages
import xlrd
from xlutils.copy import copy


def ReadFromResult(loc):
    result = xlrd.open_workbook(loc)
    sheet1 = result.sheet_by_index(0)
    rowCount = sheet1.nrows
    wb = copy(result)
    return rowCount, wb


if __name__ == '__main__':

    # set up the parameters
    vintValue = 70
    pixPerMMAtZ = 95 / 3.945
    imageWidth = 200
    imageHeight = 200

    # read an excel file, prepare to store the result into it.
    loc = "./result.xls"
    rowCount, wb = ReadFromResult(loc)
    sheet1 = wb.get_sheet(0)
    index = 0

    # repeat the test for 5 times, and store each result into "result" file
    while index < 20:
        print("**** capture images start***")
        locationID = rowCount + index
        saveLocation = './pictures/pic' + str(locationID)
        CaptureAllImages(saveLocation)
        print("**** capture images end***")

        print("**** calculating start ***")
        CalculateVolume(vintValue, pixPerMMAtZ, imageWidth, imageHeight, sheet1, rowCount + index)
        wb.save('result.xls')
        index += 1
