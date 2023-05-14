import cv2
import tkinter as tk
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from servo import Servo
import math
import time
import numpy as np

pwm = PCA9685()
pwm.setPWMFreq(50)

# servos
baseServo = Servo(pwm, 0, 73)
leftServo = Servo(pwm, 1, 92)
rightServo = Servo(pwm, 2, 130)
gripperServo = Servo(pwm, 3, 180)

base_offset = 73
left_offset = 78
right_offset = 220 # 35

gripper_length = 30
forearm_length = 80
backarm_length = 80

base_angle_last = 70
left_angle_last = 80
right_angle_last = 125

current_x_pos = 80
current_y_pos = 0
current_z_pos = 80

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
    global current_x_pos
    global current_y_pos
    global current_z_pos

    b = math.atan2(y, x) * (180/math.pi) # base angle
    l = math.sqrt(x*x + y*y)# - gripper_length # x and y extension
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
    current_x_pos = x
    current_y_pos = y
    current_z_pos = z

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
    gripperServo.setAngle(180, True)

block_height = 30
block_1_pos = (96, 82, 0)
# block_2_pos = (90, -82, 0)
block_2_pos = (65, -58, 0)

safe_height = 100

def pick_block(block_pos, level = 0):
    dest_x = block_pos[0]
    dest_y = block_pos[1]
    dest_z = block_pos[2] + level * block_height
    delay = 0.4
    # go to center first
    moveTo(dest_x, dest_y, safe_height)
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z)
    time.sleep(delay)
    gripper_handle()
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z + 20)
    moveTo(dest_x, dest_y, safe_height)

def drop_block(block_pos, level = 0):
    dest_x = block_pos[0]
    dest_y = block_pos[1]
    dest_z = block_pos[2] + level * block_height
    delay = 0.4
    # go to center first
    moveTo(block_pos[0], block_pos[1], safe_height)
    time.sleep(delay)
    moveTo(dest_x, dest_y, dest_z)
    time.sleep(delay)
    gripper_drop()
    time.sleep(delay)
    moveTo(block_pos[0], block_pos[1], dest_z + 20)
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

video_device = cv2.VideoCapture(0)
video_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

yellow = [0, 255, 255]
red = [255, 100, 100]
white = [255, 255, 255]

class UI(tk.Tk):
    def __init__(self):
        super().__init__()

        # window
        self.title("Robot Arm")

        # container
        container = tk.Frame(self)
        container.grid(row=0, column=0)

        # frames
        self.frames = {}
        self.HomePage = HomePage

        for F in {HomePage}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # put the frame in front

class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.left_controls().grid(row=0, column=0)

        self.videoLabel = tk.Label(self)
        self.videoLabel.grid(row=0, column=1)
        self.camLoop()

        self.right_controls().grid(row=0, column=2)

    def left_controls(self):
        left_controls_frame = tk.Frame(self)

        def emergency_stop():
            exit()

        button_exit = tk.Button(
                left_controls_frame, text="ACİL DURDURMA",
                command=emergency_stop, bg="red", fg="white")
        button_exit.grid(row=0, column=0, ipadx=30, ipady=20)

        def initial_position():
            moveTo(80, 0, 80)

        button_initial_position = tk.Button(
                left_controls_frame, text="BAŞLANGIÇ KONUMU", command=initial_position)
        button_initial_position.grid(row=1, column=0, ipadx=30, ipady=20)

        return left_controls_frame

    def right_controls(self):
        right_controls_frame = tk.Frame(self)

        sensetivity = tk.DoubleVar()

        def forwardCommand():
            moveTo(current_x_pos + sensetivity.get(), current_y_pos, current_z_pos)

        bForward = tk.Button(right_controls_frame, text="İLERİ", command=forwardCommand)
        bForward.grid(row=0, column=0, ipadx=30, ipady=20, pady=5, padx=5)

        def backwardCommand():
            moveTo(current_x_pos - sensetivity.get(), current_y_pos, current_z_pos)

        bBackward = tk.Button(right_controls_frame, text="GERİ", command=backwardCommand)
        bBackward.grid(row=0, column=1, ipadx=30, ipady=20, pady=5, padx=5)

        def leftCommand():
            moveTo(current_x_pos, current_y_pos - sensetivity.get(), current_z_pos)

        bLeft = tk.Button(right_controls_frame, text="SOL", command=leftCommand)
        bLeft.grid(row=1, column=0, ipadx=30, ipady=20, pady=5, padx=5)

        def rightCommand():
            moveTo(current_x_pos, current_y_pos + sensetivity.get(), current_z_pos)

        bRight = tk.Button(right_controls_frame, text="SAĞ", command=rightCommand)
        bRight.grid(row=1, column=1, ipadx=30, ipady=20, pady=5, padx=5)

        def upCommand():
            moveTo(current_x_pos, current_y_pos, current_z_pos + sensetivity.get())

        bUp = tk.Button(right_controls_frame, text="YUKARI", command=upCommand)
        bUp.grid(row=2, column=0, ipadx=30, ipady=20, pady=5)

        def downCommand():
            moveTo(current_x_pos, current_y_pos, current_z_pos - sensetivity.get())

        bDown = tk.Button(right_controls_frame, text="AŞAĞI", command=downCommand)
        bDown.grid(row=2, column=1, ipadx=30, ipady=20, pady=5)

        def gripCommand():
            gripper_handle()

        bGrip = tk.Button(right_controls_frame, text="TUT", command=gripCommand)
        bGrip.grid(row=3, column=0, ipadx=30, ipady=20, pady=5)

        def dropCommand():
            gripper_drop()

        bDrop = tk.Button(right_controls_frame, text="BIRAK", command=dropCommand)
        bDrop.grid(row=3, column=1, ipadx=30, ipady=20, pady=5)

        sensetivity_scale = tk.Scale(right_controls_frame, from_=0, to=20, orient="horizontal", variable=sensetivity)
        sensetivity_scale.grid(row=4, column=0, pady=5)

        return right_controls_frame

    def camLoop(self):
        global video_device
        _, frame = video_device.read()

        filter_coordinates = [200,120,540,360]

        # create black rectangles for grippers to prevent from red mask
        frame = cv2.rectangle(frame, (0, 480), (640, 380), (0, 0, 0), -1)
        frame = cv2.rectangle(frame, (0, 0), (640, 100), (0, 0, 0), -1)
        frame = cv2.rectangle(frame, (560, 0), (640, 480), (0, 0, 0), -1)
        frame = cv2.rectangle(frame, (
            filter_coordinates[0], filter_coordinates[1]),
            (filter_coordinates[2], filter_coordinates[3]),
            (0, 0, 0), 4)

        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color_sensitivity = 50
        red_lower = np.array([100 + color_sensitivity,100,100], dtype="uint8")
        red_upper = np.array([255 - color_sensitivity,255,255], dtype="uint8")

        color_sensitivity = 50
        white_lower = np.array([0,0,255 - color_sensitivity], dtype="uint8")
        white_upper = np.array([255,color_sensitivity,255], dtype="uint8")

        red_mask = cv2.inRange(hsv_image, red_lower, red_upper)

        captured_image = Image.fromarray(red_mask)
        bbox = captured_image.getbbox() 
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            if x1 >= filter_coordinates[0] and x2 <= filter_coordinates[2] and y1 >= filter_coordinates[1] and y2 <= filter_coordinates[3]:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

        white_mask = cv2.inRange(hsv_image, white_lower, white_upper)

        captured_image = Image.fromarray(white_mask)
        bbox = captured_image.getbbox() 
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            if x1 >= filter_coordinates[0] and x2 <= filter_coordinates[2] and y1 >= filter_coordinates[1] and y2 <= filter_coordinates[3]:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 5)



        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)
        self.videoLabel.photo_image = photo_image
        self.videoLabel.configure(image=photo_image)
        self.videoLabel.after(10, self.camLoop)

ui = UI()
ui.mainloop()

video_device.release()
