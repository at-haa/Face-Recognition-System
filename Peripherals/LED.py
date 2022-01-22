import RPi.GPIO as GPIO

class LED:
    def __init__(self, red_pin):
        GPIO.setmode(GPIO.BOARD)
        self.red_pin = red_pin
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.output(red_pin, GPIO.LOW)

    
    def red_on(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        
    def red_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)
    
        
        