import RPi.GPIO as GPIO
import time

class Keypad():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.KEYPAD = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]

        self.ROW    = [26,24,23,22]
        self.COLUMN = [21,19,10,12]

        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

     
    def getKey(self):
        for i in range(len(self.COLUMN)):
            GPIO.output(self.COLUMN[i], GPIO.HIGH)
            for j in range(len(self.ROW)):
                if(GPIO.input(self.ROW[j]) == GPIO.HIGH):
                    GPIO.output(self.COLUMN[i], GPIO.LOW)
                    return self.KEYPAD[j][i]
            GPIO.output(self.COLUMN[i], GPIO.LOW)
        return None
    
    
    def getKeyBusyWait(self):
        while True:
            digit = None
            while digit == None:
                digit = self.getKey()
            while digit == self.getKey():
                time.sleep(0.1)
            return digit


