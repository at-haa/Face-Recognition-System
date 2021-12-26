from Rpi_Face_Recognition.facial import FaceDetector


if __name__ == '__main__':
    face_detector = FaceDetector()
    c = 0
    while True:
        if face_detector.detect_face():
            print("Face Detected")
            print(c)
            c+= 1
            
