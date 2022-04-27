from CalculateVolume import CalculateVolume
from CapturePictures import CaptureAllImages
from CapturePicturesFromVideo import getImagesFromVideo
from CapturePicturesFromVideo import storeImagesIntoProcess
from CropWithAdjustment import GetArea
import xlrd
from xlutils.copy import copy
from time import time
import tkinter as tk


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
        if isSame(dic_cap, 1, 37):
            storeImagesIntoProcess(dic_cap, dic_pro)
            print("**** Capturing Images Success! ***")
        else:
            getImagesFromVideo(dic_cap)
            if isSame(dic_cap, 1, 37):
                storeImagesIntoProcess(dic_cap, dic_pro)
                print("**** Capturing Images Success! ***")
            else:
                print('Please replace the seed! Thanks!')
    else:
        CaptureAllImages(dic_cap)
        if isSame(dic_cap, 1, 37):
            storeImagesIntoProcess(dic_cap, dic_pro)
            print("**** Capturing Images Success! ***")
        else:
            CaptureAllImages(dic_cap)
            if isSame(dic_cap, 1, 37):
                storeImagesIntoProcess(dic_cap, dic_pro)
                print("**** Capturing Images Success! ***")
            else:
                print('Please replace the seed! Thanks!')

    print("**** calculating start ***")
    CalculateVolume(name, dic_pro, vintValue, pixPerMMAtZ, imageWidth, imageHeight, sheet1, startRow, save)
    print("Total time: --- %s seconds ---" % (time() - startTime) + "\n")


# function for button "run" in the UI
def running():
    print("hello")
    # singleTest(seedName, path_Process, path_CaptureImage, 'video', rowCount + 1, stored)


# set up the window
def setUpWindow(win):
    # width of window, height of window, startX, startY, rowGap, fontSize, button's width
    param = [700, 500, 10, 80, 40, 14, 10]
    resolution = 1

    param = [1750, 1250, 25, 200, 100, 14, 10]
    resolution = 2.5

    window.title('Volume Calculating')
    window.geometry('%sx%s' % (param[0], param[1]))

    startX = param[2]
    startY = param[3]
    startY_text = startY
    rowGap = param[4]
    fontSize = param[5]

    # create elements per row
    # "user name"
    tk.Label(window, text='User Name: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_usr_name = tk.StringVar()
    var_usr_name.set('example@python.com')
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name, font=('Arial', fontSize))
    entry_usr_name.place(x=startX+120*resolution, y=startY)

    # "seed type"
    startY += rowGap
    tk.Label(window, text='Seed Type: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_seed_type = tk.StringVar()
    entry_seed_type = tk.Entry(window, textvariable=var_seed_type, font=('Arial', fontSize))
    entry_seed_type.place(x=startX+120*resolution, y=startY)

    # "seed id"
    startY += rowGap
    tk.Label(window, text='Seed ID: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_seed_id = tk.StringVar()
    entry_seed_id = tk.Entry(window, textvariable=var_seed_id, font=('Arial', fontSize))
    entry_seed_id.place(x=startX+120*resolution, y=startY)

    # "whether show 3d model"
    startY += rowGap
    var_show_model = tk.StringVar()
    button_show_model = tk.Checkbutton(window, text='Show 3d Model', variable=var_show_model, onvalue=1, offvalue=0)
    button_show_model.place(x=startX+120*resolution, y=startY)

    # "run" and "exit"
    startY += rowGap
    button_run = tk.Button(window, text='Run', font=('Arial', fontSize), width=param[6], height=1, command=running)
    button_run.place(x=startX+50*resolution, y=startY)
    button_exit = tk.Button(window, text='Exit', font=('Arial', fontSize), width=param[6], height=1, command=exit)
    button_exit.place(x=(param[0]+100)/4, y=startY)

    # running text
    startY += rowGap + 10
    text_running = tk.Text(window, width=42, height=8)
    text_running.place(x=startX, y=startY)

    # display text
    text_display = tk.Text(window, width=30, height=22)
    text_display.place(x=(param[0]+100)/2, y=startY_text)


if __name__ == '__main__':

    window = tk.Tk()
    setUpWindow(window)
    window.mainloop()


    path_CaptureImage = './pic_Captured/'
    path_Process = './pic_processing/'
    stored = False  # whether store the results into the excel file
    seedName = '55-lg'

    # set up the parameters
    vintValue = 70
    pixPerMMAtZ = 59 / 3.12  # 95 / 3.945
    imageWidth = 200
    imageHeight = 200

    # read an excel file, prepare to store the result into it.
    loc = "./result_history.xls"
    rowCount, wb = ReadFromResult(loc)
    sheet1 = wb.get_sheet(0)



    # single seed test
    # singleTest(seedName, path_Process, path_CaptureImage, 'video', rowCount + 1, stored)
