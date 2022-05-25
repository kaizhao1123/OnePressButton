from HSVSegmentSeq import HSVSegmentSeq
from TurntableCarve import TurntableCarve
from CropWithAdjustment import CropWithAdjustment
from CropWithAdjustment import getExpectedValues
from datetime import datetime

import subprocess
import os.path
from sys import platform
from tkinter import messagebox

# only compile c programm on linux, binary for win32 included.
if platform != "win32":
    if not os.path.isfile("CarveIt.o"):
        p = subprocess.Popen("gcc -O3 CarveIt.c -lm -o CarveIt.o", shell=True)
        p.wait()


# Dummy class for storage
class Object(object):
    pass


##################################################################
def CalculateVolume(name, dic, vintValue, pixPerMMAtZ, imageWidth, imageHeight, show3D, stored, wb, sheet, rowCount):
    print("** Process --- Analyze images **")

    # ############ new method ##############
    allWidthData, allHeightData = getExpectedValues(dic, vintValue, "original")
    CropWithAdjustment(dic, vintValue, imageWidth, imageHeight, allWidthData)
    #
    allWidthData.sort()
    result_Length = allWidthData[35]
    result_Width = allWidthData[0]
    result_Height = sum(allHeightData) / 36

    # ############ new method ##############

    ##################################################################
    fnroi = Object()
    fnroi.base = dic + 'ROI_'
    fnroi.number = range(0, 360, 10)
    fnroi.extension = '.png'
    ##################################################################
    # initialization for 'HSVSegmentSeq'
    #
    # initial 'Mask' images
    fnmask = Object()
    fnmask.base = dic + 'Mask_'
    fnmask.number = range(0, 360, 10)
    fnmask.extension = '.png'
    # color interval of foreground object in HSV space
    Hint = [0, 255]
    Sint = [0, 255]
    Vint = [vintValue, 255]  # 75

    # segment seed using its HSV color value
    HSVSegmentSeq(fnroi, fnmask, Hint, Sint, Vint)

    # initialization for 'TurntableCarve'
    #
    # image and camera properties
    cam = Object()
    cam.alpha = range(0, -360, -10)  # rotation angle
    cam.PixPerMMAtZ = pixPerMMAtZ  # calibration value: pixel per mm at working depth: measure in image
    cam.PixPerMMSensor = 1 / 0.0069  # 4.7�m pixel size (Nikon D7000, from specs) 1/0.0062
    cam.FocalLengthInMM = 12.5  # read from lens or from calibration
    #
    # description of the reconstruction volume V as cuboid
    V = Object()
    V.VerticalOffset = 0  # Vertical offset of center of reconstruction cuboid (i.e the volume) in roi [unit: pixel]
    V.VerticalOffset_t = 10
    V.VolWidth = 10.0  # width of the volume in mm (X-direction) 10.0
    V.VolHeight = 10.0  # height of the volume in mm (Y-direction) 10.0
    V.VolDepth = 10.0  # depth of the volume in mm (Z-direction) 10.0
    V.sX = 100  # number of voxels in X-direction 100
    V.sY = 100  # number of voxels in Y-direction 100
    V.sZ = 100  # number of voxels in Z-direction 100
    #
    # perform volume carving on mask images
    volume_in_mm3 = TurntableCarve(fnmask, cam, V, imageWidth, imageHeight, show3D)
    ##################################################################

    ##################################################################
    # print result

    result_Length = result_Length / pixPerMMAtZ
    result_Width = result_Width / pixPerMMAtZ
    result_Height = result_Height / pixPerMMAtZ

    # print('length = ' + ("%0.3f" % result_Length) + 'mm\n')
    # print('width = ' + ("%0.3f" % result_Width) + 'mm\n')
    # print('height = ' + ("%0.3f" % result_Height) + 'mm\n')
    # print('Volume3D = ' + ("%0.3f" % volume_in_mm3) + 'mm^3\n')

    # store the results into excel file
    if stored:
        sheet.write(rowCount, 0, rowCount)
        sheet.write(rowCount, 1, name)
        sheet.write(rowCount, 2, result_Length)
        sheet.write(rowCount, 3, result_Width)
        sheet.write(rowCount, 4, result_Height)
        sheet.write(rowCount, 5, volume_in_mm3)
        sheet.write(rowCount, 6, str(datetime.now().date()))
        try:
            wb.save('result.xls')
        except Exception as e:
            messagebox.showerror("Save Error", "Please close the 'result' file! Otherwise can't be saved!")

    return result_Length, result_Width, result_Height, volume_in_mm3
    ##################################################################
