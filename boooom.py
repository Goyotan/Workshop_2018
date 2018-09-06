import cv2
import time
import numpy as np
from datetime import datetime, timezone, timedelta

# Color Detector
def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsvMin = np.array([0,70,50])
    hsvMax = np.array([10,255,255])
    colorFrame1 = cv2.inRange(hsv, hsvMin, hsvMax)

    hsvMin = np.array([170,70,50])
    hsvMax = np.array([180,255,255])
    colorFrame2 = cv2.inRange(hsv, hsvMin, hsvMax)

    return colorFrame1 + colorFrame2

# Motor Move
def gogo(direct):
    if(direct == "R"):
        print("R Turn")
    else:
        print("L Turn")
    
def main():
    capture = cv2.VideoCapture(0)
    #faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    capture.set(3,640) # 幅
    capture.set(4,480) # 高さ
    capture.set(5,60)  # FPS

    allow_cord = 110 # 許容値
    mid_screen = 240 # フレーム中点
    x_cord = 0 # x座標

    while(True):
        ret, image = capture.read()

        # Enable color mask
        mask = detect_color(image)
        img_color = cv2.bitwise_and(image, image, mask=mask)
        
        # To detect color area
        points = cv2.findNonZero(mask)

        # I don't want to have None
        if(not(points is None)):
            x_cord = np.ravel(points)[0]

        # 移動許容値 
        if((x_cord - mid_screen) <= allow_cord and (x_cord - mid_screen) >= -allow_cord):
            print("許容値")
            time.sleep(0.1)
        elif((x_cord - mid_screen) >= allow_cord):
            #print("右へ！")
            gogo("R")
        elif((x_cord - mid_screen) <= -allow_cord):
            #print("左へ!")
            gogo("L")

        print()
        
        # 描画
        cv2.imshow("Frame", image)
        cv2.imshow("Mask", img_color)


        # Any key type to exit
        if cv2.waitKey(10) > 0:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()