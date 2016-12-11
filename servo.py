
import RPi.GPIO as IO
import time
import sys

pin = 18
start = 3
end = 14

#Experiment with the starting and ending dutycycle, as well as the duration to sleep

gradient =float(end - start)/float(180)
print(gradient)

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(pin,IO.OUT)
p = IO.PWM(pin,50)
p.start(start)
time.sleep(2)

def survey(step):
  duty_cycle = start
  increment = step*gradient
  reverse = False
  while True:
    if(duty_cycle >= 14):
      reverse = True
    if(duty_cycle <= 3):
      reverse = False
    if reverse:
      duty_cycle -= increment
    else:
      duty_cycle += increment
    print(duty_cycle)
    p.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

survey(20)

