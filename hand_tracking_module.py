import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,handsno=2,detectionCon=0.5,trackingCon=0.5):
        self.mode = mode
        self.handsno = handsno
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.handsno,self.detectionCon,self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findposition(self, img, handNo=0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)
        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    ctime = 0
    stime = 0
    detector=handDetector()
    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findposition(img)
        if len(lmlist) != 0:
            #for printing the position of point 4 on the hand
            print(lmlist[4])
        ctime = time.time()
        fps = 1 / (ctime - stime)
        stime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
