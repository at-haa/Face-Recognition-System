from Rpi_Face_Recognition.facial import FaceDetector
import requests
from rpi_lcd import LCD
import os
import time
import subprocess

def turn_off_screen():
     os.system("sudo xset dpms force off")


def turn_on_screen():
     os.system("sudo xset dpms force on")     


def start_stream_service():
    os.system("sudo service motion start")
 
 
def stop_stream_service():
    os.system("sudo service motion stop")
    
    
def show_stream():
    os.system("DISPLAY=:0 chromium-browser -kiosk -app=http://127.0.0.1:8081 &")
    

def exit_stream():
    os.system("pkill -o chromium")


def send_photo_request():
    url = 'https://35d4e1d5-ca62-4148-99ac-fcbfe6d3758f.mock.pstmn.io/check'
    files = {'media': open('image.jpg', 'rb')}
    return requests.post(url, files=files)


if __name__ == '__main__':
    turn_off_screen()
    start_stream_service()
    time.sleep(1)
    show_stream()
    #lcd = LCD()
    #led = LED(12, 38, 40)
    face_detector = FaceDetector()
    detect_time = time.time()
    current_time = None
    detected = 0
    while True:
        if face_detector.detect_face() and detected == 0:
            detect_time = time.time()
            detected = 1
            turn_on_screen()
        current_time = time.time()
        if(current_time - detect_time > 10):
            turn_off_screen()
        
#             print(c)
#             c+= 1
#             status_code = 0
#             while status_code != 200:
#                 response = send_photo_request()
#                 try:
#                     data = response.json()
#                     status_code = response.status_code
#                     print(status_code)
#                 except requests.exceptions.RequestException:
#                     print(response.text)
    
        