import RPi.GPIO as GPIO

class LED:
    def __init__(self, red, green, blue):
        GPIO.setmode(GPIO.BCM)
        self.red = red
        self.green = green
        self.blue = blue
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)

    def set(self, r, g, b):
        GPIO.output(self.red, r)
        GPIO.output(self.green, g)
        GPIO.output(self.blue, b)
