import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from servo import Servo
import math
import time

pwm = PCA9685()
pwm.setPWMFreq(50)

# servos
baseServo = Servo(pwm, 0, 75)
leftServo = Servo(pwm, 1, 80)
rightServo = Servo(pwm, 2, 125)
gripperServo = Servo(pwm, 3, 160)

forearm_length = 8
backarm_length = 8

base_offset = 75
left_offset = 80
right_offset = 215 # 35

base_angle_last = 70
left_angle_last = 80
right_angle_last = 125

def virtual_side_length(x, z):
    return math.sqrt((x ** 2) + (z ** 2) - (2 * x * z * math.cos(90/180*math.pi)))

def func1(x, z):
    z2 = virtual_side_length(x, z)

    cosAlpha = math.degrees(math.acos((forearm_length ** 2 + backarm_length ** 2 - z2 ** 2) / (2 * forearm_length * backarm_length)))

    # lenght servo
    cosBeta = math.degrees(math.acos((backarm_length ** 2 + z2 ** 2 - forearm_length ** 2) / (2 * backarm_length * z2)))
    # height servo
    cosTheta = 180 - cosBeta - cosAlpha

    print(cosBeta, cosTheta)

    beta = 90 - cosBeta + 35
    theta = 90 - cosTheta + 80

    print(int(beta), int(theta))
    heightServo.setAngle(int(beta), True)
    lengthServo.setAngle(int(theta), True)

def setAngles(base, left, right):
    running = True
    global base_angle_last
    global left_angle_last
    global right_angle_last
    while running:
        if base_angle_last != base:
            if base_angle_last > base:
                base_angle_last -= 1            
            else:
                base_angle_last += 1            

        if left_angle_last != left:
            if left_angle_last > left:
                left_angle_last -= 1            
            else:
                left_angle_last += 1            

        if right_angle_last != right:
            if right_angle_last > right:
                right_angle_last -= 1            
            else:
                right_angle_last += 1            

        if base_angle_last == base and left_angle_last == left and right_angle_last == right:
            running = False

        baseServo.setAngle(base_angle_last, True)
        leftServo.setAngle(left_angle_last, True)
        rightServo.setAngle(right_angle_last, True)

def moveTo(x, y, z):
    b = math.atan2(y, x) * (180/math.pi) # base angle
    l = math.sqrt(x*x + y*y) # x and y extension
    h = math.sqrt(l*l + z*z)
    phi = math.atan(z/l) * (180/math.pi)
    theta = math.acos((h/2)/80) * (180/math.pi)
    a1 = phi + theta
    a2 = phi - theta

    a1 *= -1
    b *= -1

    b_servo = b + base_offset
    l_servo = a2 + left_offset
    r_servo = a1 + right_offset

    print("base => ", b, b_servo)
    print("left => ", a2, l_servo)
    print("right => ", a1, r_servo)

    setAngles(int(b_servo), int(l_servo), int(r_servo))

def program1():
    moveTo(80, 0, 5)
    time.sleep(1.5)
    gripperServo.setAngle(140, True)
    time.sleep(1.5)
    moveTo(80, 0, 80)
    moveTo(135, 0, 80)
    moveTo(135, 0, 35)
    time.sleep(1.5)
    gripperServo.setAngle(160, True)
    time.sleep(1.5)
    moveTo(80, 0, 80)

program1()
