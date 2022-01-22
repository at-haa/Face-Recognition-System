from imutils.video import VideoStream
import imutils
import time
import cv2
import urllib 
import numpy as np

class FaceDetector:

    def __init__(self):
        self.vs = VideoStream("http://127.0.0.1:8081/").start()
        time.sleep(3.0)
        self.detector = cv2.CascadeClassifier("Rpi_Face_Recognition/haarcascade_frontalface_default.xml")
    
    def detect_face(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1,
                                               minNeighbors=5, minSize=(30, 30),
                                               flags=cv2.CASCADE_SCALE_IMAGE)
       
        if len(rects) == 0:
            return False
        else:
            x1 = rects[0][0]
            y1 = rects[0][1]
            x2 = rects[0][0] + rects[0][2]
            y2 = rects[0][1] + rects[0][3]
            if not(x1 > 50 and x2 < 450) or not (y1 > 35 and y2 < 340):
                return False
            cv2.imwrite("image.jpg", frame)
            return True





