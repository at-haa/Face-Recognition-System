import RPi.GPIO as GPIO
from keypad import keypad
 
GPIO.setwarnings(False)
 
if __name__ == '__main__':
    kp = keypad(columnCount = 4) 

    while True:
        digit = None
        while digit == None:
            digit = kp.getKey()
        while digit == kp.getKey():
            pass 
        print(digit)