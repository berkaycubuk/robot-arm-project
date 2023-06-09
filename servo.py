import time

class Servo:
    delay = 0.01

    def __init__(self, pwm, pin, initialAngle = 50):
        self.pwm = pwm
        self.pin = pin
        self.angle = initialAngle
        pwm.setRotationAngle(pin, initialAngle)

    def getAngle(self):
        return pwm.read(pin)

    def setAngle(self, angle, isSmooth = False):
        if (isSmooth):
            diff = self.angle - angle
            if (diff > 0):
                for x in range(diff):
                    self.angle -= 1
                    self.pwm.setRotationAngle(self.pin, self.angle)
                    time.sleep(self.delay)
            else:
                for x in range(diff * (-1)):
                    self.angle += 1
                    self.pwm.setRotationAngle(self.pin, self.angle)
                    time.sleep(self.delay)
        else:
            self.pwm.setRotationAngle(self.pin, angle)

    def getAngle(self):
        return self.angle
