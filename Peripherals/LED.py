import RPi.GPIO as GPIO

class LED:
    def __init__(self, red_pin, green_pin, blue_pin):
        GPIO.setmode(GPIO.BOARD)
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(blue_pin, GPIO.LOW)
    
    def red_on(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        
    def red_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)
    
    def green_on(self):
        GPIO.output(self.green_pin, GPIO.HIGH)
        
    def green_off(self):
        GPIO.output(self.green_pin, GPIO.LOW)
        
    def blue_on(self):
        GPIO.output(self.blue_pin, GPIO.HIGH)
        
    def blue_off(self):
        GPIO.output(self.blue_pin, GPIO.LOW)    
        
        
        