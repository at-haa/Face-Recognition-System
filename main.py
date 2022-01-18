from Rpi_Face_Recognition.facial import FaceDetector
from Peripherals.Keypad import Keypad
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
    keypad = Keypad()
    turn_off_screen()

    start_stream_service()
    time.sleep(1)

    show_stream()

    lcd = LCD()
    lcd.clear()

    # led = LED(12, 38, 40)

    face_detector = FaceDetector()

    detect_time = time.time()
    current_time = None

    detected = 0
    keypad_str = ""
    while True:
        if face_detector.detect_face() and detected == 0:
            detect_time = time.time()
            detected = 1
            turn_on_screen()

        if detected == 1:
            lcd.text("Welcome!", 1)
            message = "                Please Look at The Camera!                "
            for i in range(50):
                lcd.text(message[i: i + 16], 2)
                time.sleep(0.1)
            lcd.clear()
            if face_detector.detect_face():
                lcd.text("Authorizing...", 1)
                time.sleep(1)  # send image to server
                lcd.clear()
                start = time.time()
                seconds = 120
                lcd.text("Enter Your Code", 2)
                new_key = None
                old_key = None
                while seconds > 0:

                    new_time = int(120 - (time.time() - start))
                    new_key = keypad.getKey()
                    if new_key != old_key and new_key != None:
                        keypad_str = keypad_str + new_key
                        lcd.text(keypad_str, 2)
                        if len(keypad_str) == 4:
                            # send code to server and check status// detected = 0 and clear lcd
                            break
                        print(keypad_str)
                    time.sleep(0.1)
                    old_key = new_key
                    if seconds - new_time >= 1:
                        seconds = new_time
                        lcd.text(str(seconds) + " Seconds Left", 1)
            else:
                lcd.clear()
                detected = 0
                turn_off_screen()

        current_time = time.time()
        if current_time - detect_time > 10 and detected == 1:
            detected = 0
            turn_off_screen()

#             status_code = 0
#             while status_code != 200:
#                 response = send_photo_request()
#                 try:
#                     data = response.json()
#                     status_code = response.status_code
#                     print(status_code)
#                 except requests.exceptions.RequestException:
#                     print(response.text)

