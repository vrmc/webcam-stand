import time

import cv2
import RPi.GPIO as IO

from servo import Servo
from webcam import Webcam

EPSILON = 50 # tolerance in no. of pixels for being off-center
DIVISION = 0.005 # division in rotation of webcam

# list of pins
SRV_PIN = 18 # servo pin

def main():
    IO.setmode(IO.BCM)

    servo = Servo(SRV_PIN)
    webcam = Webcam("haarcascade_frontalface_default.xml")

    MID_X = webcam.WIDTH / 2
    MID_Y = webcam.HEIGHT / 2

    servo.rotate(0.5)
    while True:
        cv2.waitKey(500)

        _, frame = webcam.cap.read()
        faces = webcam.detect_faces()
        print("Detected {} faces.".format(len(faces)))

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Webcam Output', frame)

        if len(faces) == 0:
            continue
        elif len(faces) == 1:
            x, y, w, h = faces[0]
            coord = ((2*x + w) / 2, (2*y + h) / 2)
        else:
            avg_x = sum((2*x + w) / 2 for x, _, w, _ in faces) / len(faces)
            avg_y = sum((2*y + h) / 2 for _, y, _, h in faces) / len(faces)
            coord = (avg_x, avg_y)

        diff = abs(coord[0] - MID_X)
        print(coord, diff)
        if diff > EPSILON:
            if coord[0] < MID_X:
                print(MID_X, "turning towards the left")
                servo.rotate_inc(DIVISION)
            elif coord[0] > MID_X:
                print(MID_X, "turning towards the right")
                servo.rotate_inc(-DIVISION)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

