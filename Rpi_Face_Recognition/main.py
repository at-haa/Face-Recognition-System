from facial import FaceDetector

if __name__ == '__main__':
    face_detector = FaceDetector()
    while True:
        if face_detector.detect_face():
            print("face Detected")
        #else:
