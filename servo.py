import time

import pigpio


class Servo:
    # Experiment with the starting and ending dutycycle (from 0 to 255)
    START = 5.6
    END = 12.7

    # for pin number, assume using IO.BCM
    def __init__(self, pin):
        self._pi = pigpio.pi()
        self.pin = pin
        self._pi.set_PWM_frequency(self.pin, 50)
        self.rotate(0.5) # set motor to midpoint
        time.sleep(1)

    def rotate(self, division):
        if division < 0 or division > 1:
            raise ValueError('division not within 0 to 1')
        self.division = division
        self.duty_cycle = (self.START + self.END) * self.division
        self._pi.set_PWM_dutycycle(self.pin, self.duty_cycle)

    def rotate_inc(self, inc_division):
        n_division = self.division + inc_division
        if n_division > 1:
            self.rotate(1)
        elif n_division < 0:
            self.rotate(0)
        else:
            self.rotate(n_division)

def main():
    srv = Servo(18)
    reverse = False 
    while True:
        if srv.duty_cycle >= srv.END:
            reverse = True
        elif srv.duty_cycle <= srv.START:
            reverse = False

        if reverse:
            srv.rotate_inc(-0.05)
        else:
            srv.rotate_inc(0.05)
        print(srv.duty_cycle)
        time.sleep(1)
    

if __name__ == "__main__":
    main()

