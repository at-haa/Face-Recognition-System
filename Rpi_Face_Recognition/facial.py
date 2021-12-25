from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
import requests


currentname = "unknown"


encodings = "encodings.pickle"
data = pickle.loads(open(encodings, "rb").read())

cascade = "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(cascade)

vs = VideoStream(usePiCamera=True).start()
time.sleep(3.0)


while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    print(encodings)
    print(type(encodings))
    for encoding in encodings:

        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            
            if currentname != name:
                currentname = name
                img_name = "image.jpg"
                cv2.imwrite(img_name, frame)
                print(currentname)
                
                
        names.append(name)

    
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)
    keyboard_input = cv2.waitKey(1)

    if (chr(keyboard_input%256).lower() == 'q'):
        break

cv2.destroyAllWindows()
vs.stop()
