from Rpi_Face_Recognition.facial import FaceDetector
import requests
from rpi_lcd import LCD
def send_photo_request():
    url = 'https://35d4e1d5-ca62-4148-99ac-fcbfe6d3758f.mock.pstmn.io/check'
    files = {'media': open('image.jpg', 'rb')}
    return requests.post(url, files=files)


if __name__ == '__main__':
    lcd = LCD()
    led = LED(12, 38, 40)
    face_detector = FaceDetector()
    c = 0
    while True:
        if face_detector.detect_face():
            lcd.text("Wait for", 1)
            lcd.text("Green Light!", 2)
            print("Face Detected")
            print(c)
            c+= 1
            status_code = 0
            while status_code != 200:
                response = send_photo_request()
                try:
                    data = response.json()
                    status_code = response.status_code
                    print(status_code)
                except requests.exceptions.RequestException:
                    print(response.text)
            
