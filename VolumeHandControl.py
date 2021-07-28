import cv2
import mediapipe as mp
import time
import numpy as np
import hand_tracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import tkinter as tk


def func():
    #size if the window
    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture(1) if an external camera is being used
    #cap = cv2.VideoCapture('http://(ip adress if the camera being used is your phone)/mjpegfeed')
    cap.set(3, wCam)
    cap.set(4, hCam)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    stime = 0

    detector=htm.handDetector(detectionCon=0.7)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volrange = volume.GetVolumeRange()
    minvol = volrange[0]
    maxvol = volrange[1]

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        img = detector.findhands(img)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 0), 2)

        lmklist=detector.findposition(img,draw=False)
        if len(lmklist)!=0:
            x1, y1 = lmklist[4][1], lmklist[4][2]
            x2, y2 = lmklist[8][1], lmklist[8][2]
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (mx, my), 10, (255, 255, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0),2)

            l = math.hypot((x2-x1), (y2-y1))

            vol = np.interp(l, [0, 250], [minvol, maxvol])
            volume.SetMasterVolumeLevel(vol, None)
            volbar = np.interp(l, [50, 250], [400, 150])
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (255, 255, 0), cv2.FILLED)

            if l<50:
                cv2.circle(img, (mx, my), 10, (255, 0, 255), cv2.FILLED)
            if l>250:
                cv2.circle(img, (mx, my), 10, (255, 0, 0), cv2.FILLED)


        ctime = time.time()
        fps = 1 / (ctime - stime)
        stime = ctime
        cv2.putText(img, "FPS:"+str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

root = tk.Tk()

canvas1 = tk.Canvas(root, width=640, height=480)
canvas1.pack()

button1 = tk.Button(text='Start', command=func, bg='brown', fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()