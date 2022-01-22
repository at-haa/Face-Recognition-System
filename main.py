from Rpi_Face_Recognition.facial import FaceDetector
from Peripherals.Keypad import Keypad
from Peripherals.LED import LED
import requests
from rpi_lcd import LCD
import os
import time

is_owner = 2


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
    url = "http://192.168.1.51:3000/v1/validateImage"
    files = {'image': open('image.jpg', 'rb')}
    global is_owner
    is_owner = 2
    try:
        res = requests.post(url, files=files)
        if res.status_code == 200:
            is_owner = 1
        elif res.status_code == 404:
            print("here")
            is_owner = 0
    except requests.exceptions.RequestException:
        print("error")
    return


def send_code_request(code):
    url = "http://192.168.1.51:3000/v1/validateCode"
    data = {"code": code}
    try:
        res = requests.post(url, data=data)
        if res.json()['result'] != "Messages Sent":
            print("Enter!!!")
            return True
        else:
            print("Wrong Code!!!")
            return False
    except requests.exceptions.RequestException:
        print("Error")
    return None


def send_phone_request(code):
    url = "http://192.168.1.51:3000/v1/validateCode"
    data = {"code": code}
    files = {'image': open('image.jpg', 'rb')}
    try:
        res = requests.post(url, data=data, files=files)
        if res.json()['result'] != "Messages Sent":
            print("Wait for the owner open the door")
            return True
        else:
            print("something went wrong")
            return False
    except requests.exceptions.RequestException:
        print("Error")
    return None


if __name__ == '__main__':

    keypad = Keypad()
    lcd = LCD()
    lcd.clear()
    led = LED(40)
    turn_off_screen()
    start_stream_service()
    time.sleep(1)
    show_stream()
    face_detector = FaceDetector()
    keypad_str = ""

    while True:
        if face_detector.detect_face():
            turn_on_screen()
            lcd.text("Welcome!", 1)
            message = "                Please Look at The Camera!                "
            for i in range(50):
                lcd.text(message[i: i + 16], 2)
                time.sleep(0.1)
            lcd.clear()
            if face_detector.detect_face():
                lcd.text("Authorizing...", 1)
                send_photo_request()
                time.sleep(2)
                print("is_owner: " + str(is_owner))
                lcd.clear()
                start = time.time()
                validation_time = 60
                seconds = validation_time
                if is_owner == 1:
                    lcd.text("Enter Your Code", 2)
                else:
                    lcd.text("Enter Phone Num", 2)
                new_key = None
                old_key = None
                while seconds > 0 and is_owner != 2:
                    elapsed_time = int(time.time() - start)
                    new_key = keypad.getKey()
                    if new_key != old_key and new_key is not None:
                        if new_key == "C":
                            keypad_str = ""
                        elif new_key == "D":
                            if len(keypad_str) > 1:
                                keypad_str = keypad_str[0:-1]
                            else:
                                keypad_str = ""
                        elif new_key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            keypad_str = keypad_str + new_key
                            if len(keypad_str) == 4 and is_owner == 1:
                                lcd.text("Validating Code...", 2)
                                result = send_code_request(keypad_str)
                                if result is None:
                                    break
                                elif result:
                                    lcd.clear()
                                    lcd.text("Welcome!", 1)
                                    lcd.text("Door Unlocked", 2)
                                    led.red_on()
                                    time.sleep(3)
                                    led.red_off()
                                    break
                                else:
                                    lcd.text("Re-Enter Code", 2)
                                    time.sleep(2)
                                    keypad_str = ""

                            elif len(keypad_str) == 11 and is_owner == 0:
                                lcd.text("Validating Phone...", 2)
                                result = send_phone_request(keypad_str)
                                if result is None or (not result):
                                    break
                                elif result:
                                    lcd.clear()
                                    lcd.text("The Owner Will!", 1)
                                    lcd.text("Open The Door!", 2)
                                    time.sleep(3)
                                    break

                        lcd.text(keypad_str, 2)
                    time.sleep(0.1)
                    old_key = new_key
                    if elapsed_time <= validation_time:
                        seconds = validation_time - elapsed_time
                        lcd.text(str(seconds) + " Seconds Left", 1)
                lcd.clear()
                keypad_str = ""
                is_owner = 2
                turn_off_screen()
            else:
                turn_off_screen()

