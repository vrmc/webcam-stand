import time
from enum import Enum

import cv2
import RPi.GPIO as GPIO

from servo import Servo
from webcam import Webcam
from switch import Button
from led import LED

EPSILON = 50 # tolerance in no. of pixels for being off-center
DIVISION = 0.01 # division in rotation of webcam

# list of pins
SRV_PIN = 18 # servo pin

class State(Enum):
    OFF = 0
    NOT_FOUND = 1
    FINDING = 2
    ADJUSTING = 3
    CENTERED = 4

def main():
    state = State.OFF
    GPIO.setmode(GPIO.BCM)

    srv = Servo(SRV_PIN)
    webcam = Webcam("haarcascade_frontalface_default.xml")
    led = LED(16, 12, 25)
    led.set(0, 0, 0)
    switch = Button(23)

    MID_X = webcam.WIDTH / 2
    MID_Y = webcam.HEIGHT / 2

    while True:
        if not switch.is_pressed():
            continue

        state = State.FINDING
        start = time.time()
        reverse = False
        while time.time() - start < 60 or state == State.ADJUSTING or state == State.CENTERED:
            _, frame = webcam.cap.read()
            faces = webcam.detect_faces()

            if len(faces) == 0:
                state = State.FINDING
                led.set(1, 1, 0)

                if srv.duty_cycle >= srv.END:
                    reverse = True
                elif srv.duty_cycle <= srv.START:
                    reverse = False

                if reverse:
                    srv.rotate_inc(-DIVISION)
                else:
                    srv.rotate_inc(DIVISION)
            else:
                start = time.time()
                state = State.ADJUSTING
                led.set(0, 1, 0)

                x, y, w, h = max(faces, key=lambda t: (t[2], t[3]))
                coord = ((2*x + w) / 2, (2*y + h) / 2)

                diff = abs(coord[0] - MID_X)
                print(coord, diff)

                if diff > EPSILON:
                    if coord[0] < MID_X:
                        print(MID_X, "turning towards the left")
                        srv.rotate_inc(DIVISION)
                    elif coord[0] > MID_X:
                        print(MID_X, "turning towards the right")
                        srv.rotate_inc(-DIVISION)
                else:
                    state = State.CENTERED

            time.sleep(0.25)

    led.set(0, 0, 0)
    state = State.OFF

if __name__ == "__main__":
    main()

