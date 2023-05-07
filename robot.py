import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from servo import Servo
import math
import torch
import numpy as np
from net import Net

class Robot:
    xPos = 0
    yPos = 0
    zPos = 0
    model_state_dict = torch.load("./model.pth")
    net = Net()
    net.load_state_dict(model_state_dict)
    net.eval()

    def __init__(self):
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(50)
        self.__setServos()

    def __setServos(self):
        self.bodyRotationServo = Servo(self.pwm, 0, 70)
        self.heightServo = Servo(self.pwm, 1, 40)
        self.lengthServo = Servo(self.pwm, 2, 120)
        self.gripperServo = Servo(self.pwm, 3, 160)

    def moveToAngle(self, base, arm1, arm2):
        self.bodyRotationServo.setAngle(base, True)
        self.heightServo.setAngle(arm1, True)
        self.lengthServo.setAngle(arm2, True)

    def moveToPosition(self, x, y, z):
        coordinates = np.array([x, y, z])
        prediction = self.net(torch.tensor(coordinates, dtype=torch.float32) / 20.0)
        angles = prediction * 360.0
        output = angles.detach().numpy()
        output = output.astype(int)
        print(output)
        self.moveToAngle(output[0], output[1], output[2])

    def moveToXPosition(self, x):
        self.moveToPosition(x, self.yPos, self.zPos)

    def pick(self):
        self.gripperServo.setAngle(142, True)

    def drop(self):
        self.gripperServo.setAngle(180, True)

    def conveyorPickReady(self):
        self.bodyRotationServo.setAngle(70, True)
        self.lengthServo.setAngle(110, True)
        self.heightServo.setAngle(120, True)

    def conveyorPick(self):
        self.bodyRotationServo.setAngle(70, True)
        self.heightServo.setAngle(40, True)
        self.lengthServo.setAngle(165, True)
        self.pick()

    def conveyorDrop(self):
        self.bodyRotationServo.setAngle(70, True)
        self.heightServo.setAngle(40, True)
        self.lengthServo.setAngle(165, True)
        self.drop()

    def moveToArea(self):
        self.bodyRotationServo.setAngle(170, True)
        self.lengthServo.setAngle(110, True)
        self.heightServo.setAngle(120, True)

    def moveToAreaDrop(self, level = 0):
        self.bodyRotationServo.setAngle(170, True)
        if level == 0:
            self.heightServo.setAngle(40, True)
            self.lengthServo.setAngle(165, True)
        if level == 1:
            self.heightServo.setAngle(60, True)
            self.lengthServo.setAngle(170, True)
        self.drop()

    def moveToAreaPick(self):
        self.bodyRotationServo.setAngle(170, True)
        self.heightServo.setAngle(40, True)
        self.lengthServo.setAngle(165, True)
        self.pick()

    def process1(self, level = 0):
        self.conveyorPick()
        self.conveyorPickReady()
        self.moveToArea()
        self.moveToAreaDrop(level)
        self.moveToArea()
        self.conveyorPickReady()
        self.conveyorDrop()

    def center(self):
        self.moveToPosition(9.0, 0.0, 6.0)

    def close(self):
        self.pwm.exit_PCA9685()
