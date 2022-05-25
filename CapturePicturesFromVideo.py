import cv2
import serial
import time


# 1st, control the motor to rotate over more than one round (540 degrees) and capture the videos.
# 2nd, deal with the video: Ignore the beginning part and the end part, leave the middle part of the video,
# which corresponds to precisely one round (360 degrees) because there is acceleration when the motor starts to turn
# and slow down before it ends.
# 3rd, read and store the 36 frames (images) from the video.
def getImagesFromVideo(dic):
    # open the camera, start to get the video
    videoCapture = cv2.VideoCapture(1)

    # set up the motor: speed/frame. # 32/5 ; 39.5/4 ; 52.6/3 ; 79/2(best).
    turnDegrees = 540
    turn = 'G21G91G1X{}F79'.format((turnDegrees * 0.08884) / 10)    # 0.08884 corresponds to 10 degrees.
    connection = serial.Serial('COM7', 115200)  # 6
    time.sleep(2)  # Wait for grbl to initialize

    # send G-code
    connection.flushInput()  # Flush startup text in serial input
    connection.write((turn + '\n').encode('utf-8'))
    # grbl_out = connection.readline()
    connection.close()

    # store the images
    i = 0
    j = 1
    while videoCapture.isOpened():
        success, frame = videoCapture.read()
        timeF = 2
        if i > timeF * 9 and i % timeF == 0:
            if j < 38:
                cv2.imwrite(dic + "/00{:02d}.bmp".format(j), frame)
                image = cv2.imread(dic + "/00{:02d}.bmp".format(j))
                crop = image[0:243, 0:720]
                cv2.imwrite(dic + "/00{:02d}.bmp".format(j), crop)
                print("img output: %d" % j)
            j += 1
        i += 1
        if i > timeF * turnDegrees / 10:
            break
    videoCapture.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


#
def storeImagesIntoProcess(dic_cap, dic_pro):
    imageNum = 1
    while imageNum < 37:
        image = cv2.imread(dic_cap + "/00{:02d}.bmp".format(imageNum))
        cv2.imwrite(dic_pro + "/00{:02d}.bmp".format(imageNum), image)
        imageNum += 1

