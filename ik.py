import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from servo import Servo
import math
import time

pwm = PCA9685()
pwm.setPWMFreq(50)

# servos
baseServo = Servo(pwm, 0, 75)
leftServo = Servo(pwm, 1, 100)
rightServo = Servo(pwm, 2, 125)
gripperServo = Servo(pwm, 3, 160)

base_offset = 75
left_offset = 80
right_offset = 215 # 35

gripper_length = 30
forearm_length = 80
backarm_length = 80

base_angle_last = 70
left_angle_last = 80
right_angle_last = 125

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
    l = math.sqrt(x*x + y*y) - gripper_length # x and y extension
    h = math.sqrt(l*l + z*z)
    phi = math.atan(z/l) * (180/math.pi)
    theta = math.acos((h/2)/80) * (180/math.pi)
    # theta = (backarm_length*backarm_length + h*h - forearm_length*forearm_length) / (2 * backarm_length * h) * (180/math.pi)

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

def gripper_handle():
    gripperServo.setAngle(138, True)

def gripper_drop():
    gripperServo.setAngle(160, True)

block_height = 25
block_1_pos = (96, 82, 3)
block_2_pos = (90, -82, 5)

safe_height = block_height * 5

def pick_block(block_pos, level = 0):
    dest_x = block_pos[0]
    dest_y = block_pos[1]
    dest_z = block_pos[2] + level * block_height
    if level == 0:
        if dest_x < 0:
            dest_x += 3
        else:
            dest_x -= 3
        if dest_y < 0:
            dest_y += 3
        else:
            dest_y -= 3
    drop_offset_x = 10
    drop_offset_y = 10
    if dest_x < 0:
        drop_offset_x = -10
    if dest_y < 0:
        drop_offset_y = -10

    delay = 0.4
    # go to center first
    moveTo(dest_x, dest_y, safe_height)
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z)
    time.sleep(delay)
    gripper_handle()
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z + 20)
    moveTo(dest_x - drop_offset_x, dest_y - drop_offset_y, dest_z + 20)
    moveTo(dest_x, dest_y, safe_height)

def drop_block(block_pos, level = 0):
    dest_x = block_pos[0]
    dest_y = block_pos[1]
    dest_z = block_pos[2] + level * block_height + 10

    if level == 3:
        if dest_x < 0:
            dest_x += 6
        else:
            dest_x -= 6
        if dest_y < 0:
            dest_y += 9
        else:
            dest_y -= 9

    if level == 2:
        if dest_x < 0:
            dest_x += 2
        else:
            dest_x -= 2
        if dest_y < 0:
            dest_y += 3
        else:
            dest_y -= 3

    if level == 0:
        if dest_x < 0:
            dest_x += 3
        else:
            dest_x -= 3
        if dest_y < 0:
            dest_y += 2
        else:
            dest_y -= 2

    drop_offset_x = 10
    drop_offset_y = 10
    if dest_x < 0:
        drop_offset_x = -10
    if dest_y < 0:
        drop_offset_y = -10

    delay = 0.4
    # go to center first
    moveTo(block_pos[0], block_pos[1], safe_height)
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z)
    time.sleep(delay)
    gripper_drop()
    time.sleep(delay)
    moveTo(block_pos[0], block_pos[1], dest_z + 20)
    moveTo(block_pos[0] - drop_offset_x, block_pos[1] - drop_offset_y, dest_z + 20)
    moveTo(block_pos[0], block_pos[1], safe_height)

def program1():
    pick_block(block_1_pos, 2)
    drop_block(block_2_pos, 1)
    pick_block(block_1_pos, 1)
    drop_block(block_2_pos, 2)
    pick_block(block_1_pos)
    drop_block(block_2_pos, 3)

def program2():
    pick_block(block_2_pos, 3)
    drop_block(block_1_pos)
    pick_block(block_2_pos, 2)
    drop_block(block_1_pos, 1)
    pick_block(block_2_pos, 1)
    drop_block(block_1_pos, 2)

program1()
program2()
time.sleep(5)
program1()
program2()
