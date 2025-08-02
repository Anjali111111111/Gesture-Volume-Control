import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(self,mode=False,maxhands =2,detectioncon=0.5,trackcon=0.5): # false mode for dynamic hand tracking

                self.mode = mode
                self.maxHands = maxhands
                self.detectioncon = detectioncon
                self.trackcon = trackcon

                self.mpHands = mp.solutions.hands
                self.hands = self.mpHands.Hands(
                    static_image_mode=self.mode,
                    max_num_hands=self.maxHands,
                    min_detection_confidence=self.detectioncon,
                    min_tracking_confidence=self.trackcon
                )
                self.mpDraw = mp.solutions.drawing_utils





    def findhands(self,img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert the image from bgr(open cv) to rgb(mediapipe format)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks: # contains the detected hand landmarks
            for handLms in self.results.multi_hand_landmarks:
               if draw:
                     self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) #draw the landmarks and connections on the original image

        return img

    def findpos(self,img,handno=0,draw= True): # extract landmark position for a specific hand

        lmList=[] #stores the landmark position
        if self.results.multi_hand_landmarks:
           myhand= self.results.multi_hand_landmarks[handno]
           for id, lm in enumerate(myhand.landmark):
                   # print(id,lm)
                   h, w, c = img.shape
                   cx, cy = int(lm.x * w), int(lm.y * h)
                   # print(id, cx, cy)
                   lmList.append([id,cx,cy])
                   if draw:
                          cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lmList

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector=handDetector()

    while True:
        success, img = cap.read()
        img=detector.findhands(img)
        lmList =detector.findpos(img)

        if len(lmList) !=0:
           print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("volume control frame",img)
        cv2.waitKey(1)



if __name__ =="__main__":
    import cv2
    import mediapipe as mp
    import time


    class handDetector:
        def __init__(self, mode=False, maxhands=2, detectioncon=0.5, trackcon=0.5):

            self.mode = mode
            self.maxHands = maxhands
            self.detectioncon = detectioncon
            self.trackcon = trackcon

            self.mpHands = mp.solutions.hands
            self.hands = self.mpHands.Hands(
                static_image_mode=self.mode,
                max_num_hands=self.maxHands,
                min_detection_confidence=self.detectioncon,
                min_tracking_confidence=self.trackcon
            )
            self.mpDraw = mp.solutions.drawing_utils

        '''  self.mode= mode
            self.maxHands =maxhands
            self.detectioncon= detectioncon
            self.trackcon= trackcon

            self.mpHands = mp.solutions.hands
            self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectioncon,self.trackcon )
            self.mpDraw = mp.solutions.drawing_utils'''

        def findhands(self, img, draw=True):

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

            return img

        def findpos(self, img, handno=0, draw=True):

            lmList = []
            if self.results.multi_hand_landmarks:
                myhand = self.results.multi_hand_landmarks[handno]
                for id, lm in enumerate(myhand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            return lmList


    def main():
        pTime = 0
        cTime = 0

        cap = cv2.VideoCapture(0)
        detector = handDetector()

        while True:
            success, img = cap.read()
            img = detector.findhands(img)
            lmList = detector.findpos(img)

            if len(lmList) != 0:
                print(lmList[4])

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.imshow("volume control frame", img)
            cv2.waitKey(1)


    if __name__ == "__main__":
            main()