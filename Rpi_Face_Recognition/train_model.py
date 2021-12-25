from imutils import paths
import face_recognition
import pickle
import cv2
import os

image_paths = list(paths.list_images("dataset"))


known_face_encodings = []
known_face_names = []

for image_path in image_paths:
    name = os.path.normpath(image_path).split(os.path.sep)[1]
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings:
        known_face_encodings.append(encoding)
        known_face_names.append(name)

data = {"encodings": known_face_encodings, "names": known_face_names}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
