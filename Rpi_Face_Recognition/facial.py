from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
import requests


class FaceDetector:

    def __init__(self):
        self.vs = VideoStream(usePiCamera=True).start()
        time.sleep(3.0)
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def detect_face(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1,
                                               minNeighbors=5, minSize=(30, 30),
                                               flags=cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return False
        else:
            cv2.imwrite("image.jpg", frame)
            return True

        # box = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        box = (rects[0][1], rects[0][0] + rects[0][2], rects[0][1] + rects[0][3] + rects[0][0])

        encodings = face_recognition.face_encodings(rgb, box)

        cv2.imwrite("image.jpg", frame)


cv2.destroyAllWindows()
vs.stop()
