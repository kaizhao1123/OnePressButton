from CalculateVolume import CalculateVolume
from CapturePictures import CaptureAllImages
from CapturePicturesFromVideo import getImagesFromVideo
from CapturePicturesFromVideo import storeImagesIntoProcess
from CropWithAdjustment import GetArea
import xlrd
from xlutils.copy import copy
from time import time
import tkinter as tk
from tkinter import END
from tkinter import messagebox
import sys


# open the excel file.
def ReadFromResult(file):
    try:
        result = xlrd.open_workbook(file)
        sheet1 = result.sheet_by_index(0)
        rowCount = sheet1.nrows
        wb = copy(result)
        return rowCount, wb
    except Exception as e:
        messagebox.showerror("Read Error", "Please close the result file!")


# setup the some default parameters
root_path = 'C:/Users/Kai Zhao/PycharmProjects/OnePressButton/'
path_Capture = root_path + 'pic_Captured/'
path_Process = root_path + 'pic_processing/'
fileName = root_path + 'dist/result.xls'     # read an excel file, prepare to store the result into it.
stored = True  # whether store the results into the excel file
captureSrc = 'video'
vintValue = 70      # the light's value (strong or weak)
pixPerMMAtZ = 59 / 3.12  # 95 / 3.945
imageWidth = 200
imageHeight = 200


# check whether two images are the same or not, to test whether the object moved during the capturing process or not.
def isSame(dic, num1, num2):
    X_1, Y_1, width_1, height_1 = GetArea(dic, vintValue, num1, "original")
    # print(X_1, Y_1, width_1, height_1)
    X_2, Y_2, width_2, height_2 = GetArea(dic, vintValue, num2, "original")
    # print(X_2, Y_2, width_2, height_2)
    if abs(X_1 - X_2 > 1) or abs(Y_1 - Y_2 > 1) or abs(width_1 - width_2 > 1) or abs(height_1 - height_2 > 1):
        print("The seed moved during the rotation!! Start to 2nd capture of the seed...")
        return False
    else:
        return True


# single seed test of volume.
def singleTest(name, dic_pro, dic_cap, imageOrFrame, show3D, save, excelfile, excelSheet, sheetRow):
    startTime = time()
    print("** Process --- Capture images **")
    if imageOrFrame == 'video':
        getImagesFromVideo(dic_cap)
        if isSame(dic_cap, 1, 37):
            storeImagesIntoProcess(dic_cap, dic_pro)
            print("** Capturing Images Success! **\n")
        else:
            getImagesFromVideo(dic_cap)
            if isSame(dic_cap, 1, 37):
                storeImagesIntoProcess(dic_cap, dic_pro)
                print("** Capturing Images Success! **")
            else:
                print('Process terminated. Please replace the seed! Thanks!')
    else:
        CaptureAllImages(dic_cap)
        if isSame(dic_cap, 1, 37):
            storeImagesIntoProcess(dic_cap, dic_pro)
            print("** Capturing Images Success! **")
        else:
            CaptureAllImages(dic_cap)
            if isSame(dic_cap, 1, 37):
                storeImagesIntoProcess(dic_cap, dic_pro)
                print("** Capturing Images Success! **")
            else:
                print('Process terminated. Please replace the seed! Thanks!')

    l, w, h, v = CalculateVolume(name, dic_pro, vintValue, pixPerMMAtZ, imageWidth, imageHeight, show3D,
                                 save, excelfile, excelSheet, sheetRow)
    print("Total time: --- %0.3f seconds ---" % (time() - startTime) + "\n")
    print("The calculation of %s " % name + " is complete!")
    return l, w, h, v


# set up the window
def setUpWindow():
    window = tk.Tk()

    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    print(height)
    print(width)

    # the elements: width of window, height of window, startX, startY, rowGap, fontSize, button's width,
    #               text_display's width, text_display's height, text_running's width, text_running's height.
    param = [round(width * 0.45), round(height * 0.6), 10, 80, 40, 14, 10, 23, 18, 42, 11]
    resolution = 1

    # when using package mayavi.mlab in file "TurntableCarve"
    # param = [round(width * 0.45), round(height * 0.6), 25, 200, 100, 14, 10, 30, 20, 42, 15]
    # resolution = 2.5

    window.title('Volume Calculating')
    window.geometry('%sx%s' % (param[0], param[1]))

    startX = param[2]
    startY = param[3]
    rowGap = param[4]
    fontSize = param[5]

    # #################  create elements per row ##############################################

    # display text, to show the result ########################################################
    text_display = tk.Text(window, font=('Arial', fontSize), width=param[7], height=param[8])
    text_display.configure(state='disabled')
    text_display.place(x=(param[0] + 100) / 2, y=startY)

    # "user name" #############################################################################
    tk.Label(window, text='User Name: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_usr_name = tk.StringVar()
    var_usr_name.set(' ')
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name, font=('Arial', fontSize))
    entry_usr_name.place(x=startX + 120 * resolution, y=startY)

    # "seed type" #############################################################################
    startY += rowGap
    tk.Label(window, text='Seed Type: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_seed_type = tk.StringVar()
    entry_seed_type = tk.Entry(window, textvariable=var_seed_type, font=('Arial', fontSize))
    entry_seed_type.place(x=startX + 120 * resolution, y=startY)

    # "seed id" ###############################################################################
    startY += rowGap
    tk.Label(window, text='Seed ID: ', font=('Arial', fontSize)).place(x=startX, y=startY)
    var_seed_id = tk.StringVar()
    entry_seed_id = tk.Entry(window, textvariable=var_seed_id, font=('Arial', fontSize))
    entry_seed_id.place(x=startX + 120 * resolution, y=startY)

    # "whether show 3d model" ##################################################################
    startY += rowGap
    var_show_model = tk.IntVar()
    button_show_model = tk.Checkbutton(window, text='Show 3d Model', variable=var_show_model)
    button_show_model.place(x=startX + 120 * resolution, y=startY)

    # running text #############################################################################
    startY += rowGap + 10
    startY += rowGap + 10
    text_running = tk.Text(window, width=param[9], height=param[10])
    text_running.configure(state='disabled')
    text_running.place(x=startX, y=startY)

    # Redirect class.
    # To show the detail(print) of the process.
    class myStdout():
        def __init__(self):
            # back it up
            self.stdoutbak = sys.stdout
            self.stderrbak = sys.stderr
            # redirect
            sys.stdout = self
            sys.stderr = self

        def write(self, info):  # The info is the output info received by the standard output sys.stdout and sys.stderr.
            # Insert a print message in the last line of the text.
            text_running.insert('end', info)
            # Update the text, otherwise, the inserted information cannot be displayed.
            text_running.update()
            # Always display the last line, otherwise, when the text overflows the last line of the control,
            # the last line will not be automatically displayed
            text_running.see(tk.END)

        def restoreStd(self):
            # Restore standard output.
            sys.stdout = self.stdoutbak
            sys.stderr = self.stderrbak

    mystd = myStdout()  # instantiate the redirect class.

    # button: "run" and "exit" #################################################################
    startY -= (rowGap + 10)

    def running():  # function for button "run" in the UI.

        rowCount, wb = ReadFromResult(fileName)
        sheet1 = wb.get_sheet(0)

        # clear the content of texts before new test.
        text_display.configure(state='normal')
        text_display.delete(1.0, END)
        text_running.configure(state='normal')
        text_running.delete(1.0, END)

        # run the volume calculation function.
        seed_t = var_seed_type.get()
        seed_id = var_seed_id.get()
        seed_name = seed_t + ": " + seed_id
        showModel = var_show_model.get()
        if showModel == 1:
            displayModel = True
        else:
            displayModel = False

        l, w, h, v = singleTest(seed_id, path_Process, path_Capture, captureSrc, displayModel,
                                stored, wb, sheet1, rowCount)

        # display the result on the display text.
        res_length = 'Length       =    ' + ("%0.3f" % l) + ' mm\n\n'
        res_width = 'Width         =    ' + ("%0.3f" % w) + ' mm\n\n'
        res_height = 'Thickness  =    ' + ("%0.3f" % h) + ' mm\n\n'
        res_volume = 'Volume3D  =  ' + ("%0.3f" % v) + ' mm^3\n\n'

        text_display.insert('insert', seed_name + '\n\n\n')
        text_display.insert('insert', res_length)
        text_display.insert('insert', res_width)
        text_display.insert('insert', res_height)
        text_display.insert('insert', res_volume)

        # initial to empty
        # var_usr_name.set(' ')
        # var_seed_type.set(' ')
        # var_seed_id.set(' ')
        text_display.configure(state='disabled')
        text_running.configure(state='disabled')

    button_run = tk.Button(window, text='Run', font=('Arial', fontSize), width=param[6], height=1,
                           command=running)
    button_run.place(x=startX + 50 * resolution, y=startY)

    button_exit = tk.Button(window, text='Exit', font=('Arial', fontSize), width=param[6], height=1,
                            command=window.quit)
    button_exit.place(x=(param[0] + 100) / 4, y=startY)

    ###########################################################################################
    window.mainloop()
    mystd.restoreStd()  # Restore standard output.
    # #################################      END      #########################################


if __name__ == '__main__':
    setUpWindow()
