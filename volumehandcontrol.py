import cv2 #importing open cv
import time # to calculate fps
import numpy as np #to convert the length between thumb and index finger into corresponding volume
import gesture_basic_module as gbm # to use handtracking method
import math #to calculate length
from ctypes import cast, POINTER #used to interact with system audio API
from comtypes import CLSCTX_ALL #
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam =640, 480 # webcam height and width
#################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam) # frame height
cap.set(4, hCam) # frame width
pTime = 0

detector = gbm.handDetector(detectioncon=0.7) #optimal value chosen to maintain accuracy and system confidence to respond


devices =  AudioUtilities.GetSpeakers() # fetch default speaker of the device
interface =  devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # prepare interface to control audio
volume = cast(interface, POINTER(IAudioEndpointVolume)) # volume is an object to control audio volume
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400 # setting the bar position at bottom for showing min volume
volPer = 0
while True:
    success, img  = cap.read()
    img = detector.findhands(img)
    lmlist = detector.findpos(img, draw=False)
    if len(lmlist)!=0:
      #print(lmlist[4],lmlist[8])

      x1, y1 = lmlist[4][1], lmlist[4][2] # coordinates of thumb
      x2, y2 = lmlist[8][1], lmlist[8][2] #coordinates of index finger
      cx, cy = (x1 + x2) // 2, (y1 +y2) // 2 # mid point calculation

      cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
      cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
      cv2.line(img, (x1, y1), (x2, y2), (255, 0 , 255), 3)
      cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED) #mid point pink

      length = math.hypot(x2-x1, y2-y1)


      #hand range 15 - 150
      #volume range -63 - 0
      # the ranges of distance between thumb and index finger linking to bar range and percent range.
      #converting length to corresponding volume using numpy
      vol = np.interp(length,[15,150],[minVol, maxVol])
      volBar = np.interp(length, [15,150], [400, 150])
      volPer = np.interp(length, [15, 150], [0, 100])
      print(int (length), vol)
      volume.SetMasterVolumeLevel(vol, None) # adjusting system volume based on calculated value

      if length <=15:
          cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED) # green circle on min volume distance

    cv2.rectangle(img, (58, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (58, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 458), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0 ,0), 3)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)

