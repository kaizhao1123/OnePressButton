from CalculateVolume import CalculateVolume
from CapturePictures import CaptureAllImages
import xlrd
from xlwt import Workbook
from xlutils.copy import copy

def ReadFromResult(loc):
    result = xlrd.open_workbook(loc)
    sheet1 = result.sheet_by_index(0)
    rowCount = sheet1.nrows
    wb = copy(result)
    return rowCount, wb


if __name__ == '__main__':
    print("**** capture images start***")
    CaptureAllImages()
    print("**** capture images end***")

    print("**** calculating start ***")
    vintValue = 105
    pixPerMMAtZ = 94 / 3.94
    imageLength = 200
    imageWidth = 200

    loc = "./result.xls"
    rowCount, wb = ReadFromResult(loc)
    sheet1 = wb.get_sheet(0)
    CalculateVolume(vintValue, pixPerMMAtZ, imageLength, imageWidth, sheet1, rowCount)
    wb.save('result.xls')
