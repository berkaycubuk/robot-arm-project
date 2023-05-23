import tkinter as tk
import time
from robo_arm.controls import Controls

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Arm")
        self.controls = Controls()

        self.left_controls().grid(row=0, column=0)

        self.videoLabel = tk.Label(self)
        self.videoLabel.grid(row=0, column=1)
        #self.camLoop()

        self.right_controls().grid(row=0, column=2)

    def left_controls(self):
        left_controls_frame = tk.Frame(self)

        def emergency_stop():
            self.controls.__del__()
            exit()

        button_exit = tk.Button(
                left_controls_frame, text="ACİL DURDURMA",
                command=emergency_stop, bg="red", fg="white")
        button_exit.grid(row=0, column=0, ipadx=30, ipady=20)

        def initial_position():
            self.controls.move_to(80, 0, 80)

        button_initial_position = tk.Button(
                left_controls_frame, text="BAŞLANGIÇ KONUMU", command=initial_position)
        button_initial_position.grid(row=1, column=0, ipadx=30, ipady=20)

        def program_one():
            # step 1
            self.controls.move_to(80, 0, 5)
            time.sleep(0.5)
            self.controls.gripper_pick()
            time.sleep(0.5)
            self.controls.move_to(80, 0, 80)
            self.controls.move_to(90, 50, 80)
            time.sleep(0.5)
            self.controls.move_to(90, 50, 5)
            time.sleep(0.5)
            self.controls.gripper_drop()
            time.sleep(0.5)
            self.controls.move_to(90, 50, 80)
            self.controls.move_to(80, 0, 80)

            # step 2
            self.controls.move_to(80, 0, 5)
            time.sleep(0.5)
            self.controls.gripper_pick()
            time.sleep(0.5)
            self.controls.move_to(80, 0, 80)
            self.controls.move_to(90, 50, 80)
            time.sleep(0.5)
            self.controls.move_to(90, 50, 25)
            time.sleep(0.5)
            self.controls.gripper_drop()
            time.sleep(0.5)
            self.controls.move_to(90, 50, 80)
            self.controls.move_to(80, 0, 80)

        button_program_one = tk.Button(
                left_controls_frame, text="PROGRAM 1", command=program_one)
        button_program_one.grid(row=2, column=0, ipadx=30, ipady=20)

        return left_controls_frame

    def right_controls(self):
        right_controls_frame = tk.Frame(self)

        sensetivity = tk.DoubleVar()

        def forwardCommand():
            self.controls.move_forward(sensetivity.get())

        bForward = tk.Button(right_controls_frame, text="İLERİ", command=forwardCommand)
        bForward.grid(row=0, column=0, ipadx=30, ipady=20, pady=5, padx=5)

        def backwardCommand():
            self.controls.move_backward(sensetivity.get())

        bBackward = tk.Button(right_controls_frame, text="GERİ", command=backwardCommand)
        bBackward.grid(row=0, column=1, ipadx=30, ipady=20, pady=5, padx=5)

        def leftCommand():
            self.controls.move_left(sensetivity.get())

        bLeft = tk.Button(right_controls_frame, text="SOL", command=leftCommand)
        bLeft.grid(row=1, column=0, ipadx=30, ipady=20, pady=5, padx=5)

        def rightCommand():
            self.controls.move_right(sensetivity.get())

        bRight = tk.Button(right_controls_frame, text="SAĞ", command=rightCommand)
        bRight.grid(row=1, column=1, ipadx=30, ipady=20, pady=5, padx=5)

        def upCommand():
            self.controls.move_up(sensetivity.get())

        bUp = tk.Button(right_controls_frame, text="YUKARI", command=upCommand)
        bUp.grid(row=2, column=0, ipadx=30, ipady=20, pady=5)

        def downCommand():
            self.controls.move_down(sensetivity.get())

        bDown = tk.Button(right_controls_frame, text="AŞAĞI", command=downCommand)
        bDown.grid(row=2, column=1, ipadx=30, ipady=20, pady=5)

        def gripCommand():
            self.controls.gripper_pick()

        bGrip = tk.Button(right_controls_frame, text="TUT", command=gripCommand)
        bGrip.grid(row=3, column=0, ipadx=30, ipady=20, pady=5)

        def dropCommand():
            self.controls.gripper_drop()

        bDrop = tk.Button(right_controls_frame, text="BIRAK", command=dropCommand)
        bDrop.grid(row=3, column=1, ipadx=30, ipady=20, pady=5)

        sensetivity_scale = tk.Scale(right_controls_frame, from_=0, to=20, orient="horizontal", variable=sensetivity)
        sensetivity_scale.grid(row=4, column=0, pady=5)

        return right_controls_frame
