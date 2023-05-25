import tkinter as tk
from tkinter import ttk
import time
from robo_arm.controls import Controls
from robo_arm.camera import Camera
import cv2
from PIL import Image, ImageTk
import numpy as np

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Arm")

        notebook = ttk.Notebook(self)
        notebook.pack()

        frame1 = tk.Frame(notebook)
        control_page = ControlPage(self, frame1).grid(row=0,column=0)
        notebook.add(frame1, text='Kontroller')

        frame2 = tk.Frame(notebook)
        editor_page = EditorPage(self, frame2).grid(row=0,column=0)
        notebook.add(frame2, text='Editör')

        notebook.enable_traversal()

class EditorPage(tk.Frame):
    def __init__(self, root, container):
        super().__init__(container)

        blocks = []

        blocks_listbox = tk.Listbox(self)
        blocks_listbox.grid(row=0,column=0)

        add_block_name_label = tk.Label(self, text="Blok adı").grid(row=0,column=1)
        block_name = tk.StringVar()
        add_block_name = tk.Entry(self, textvariable=block_name).grid(row=0, column=2)
        block_x = tk.StringVar()
        add_block_x_label = tk.Label(self, text="x konumu").grid(row=1,column=1)
        add_block_x = tk.Entry(self, textvariable=block_x).grid(row=1, column=2)
        block_y = tk.StringVar()
        add_block_y_label = tk.Label(self, text="y konumu").grid(row=2,column=1)
        add_block_y = tk.Entry(self, textvariable=block_y).grid(row=2, column=2)
        block_level = tk.StringVar()
        add_block_level_label = tk.Label(self, text="blok seviyesi").grid(row=3,column=1)
        add_block_level = tk.Entry(self, textvariable=block_level).grid(row=3, column=2)

        def add_block():
            blocks.append({
                'name': block_name.get(),
                'x': block_x.get(),
                'y': block_y.get(),
                'level': block_level.get()
            })
            blocks_listbox.insert(tk.END, block_name.get())
        add_block_button = tk.Button(self, text="blok ekle", command=add_block).grid(row=4,column=1)

        def delete_block():
            if blocks_listbox.curselection() is None:
                return
            for item in blocks:
                if blocks_listbox.get(blocks_listbox.curselection()[0]) == item['name']:
                    blocks.remove(item)
            blocks_listbox.delete(blocks_listbox.curselection()[0])
        delete_block_button = tk.Button(self, text="Bloğu sil", command=delete_block).grid(row=1,column=0)

class ControlPage(tk.Frame):
    def __init__(self, root, container):
        super().__init__(container)
        self.controls = Controls()
        self.camera = Camera()

        self.left_controls().grid(row=0, column=0)

        self.videoLabel = tk.Label(self)
        self.videoLabel.grid(row=0, column=1)
        self.cam_loop()

        self.right_controls().grid(row=0, column=2)

    def cam_loop(self):
        frame = self.camera.read()
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # captured_image = Image.fromarray(hsv)
        # photo_image = ImageTk.PhotoImage(image=captured_image)
        # self.videoLabel.photo_image = photo_image
        # self.videoLabel.configure(image=photo_image)
        # self.videoLabel.after(10, self.cam_loop)

        # edge detection

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(
        #         hsv,
        #         np.array([100 + 50,100,100], dtype="uint8"),
        #         np.array([255 - 50,255,255], dtype="uint8"))
        # edges = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),50,200) 
        # captured_image = Image.fromarray(edges)
        # photo_image = ImageTk.PhotoImage(image=captured_image)
        # self.videoLabel.photo_image = photo_image
        # self.videoLabel.configure(image=photo_image)
        # self.videoLabel.after(10, self.cam_loop)

        # contour experiment

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # contours, _ = cv2.findContours(
        #         threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # i = 0

        # for contour in contours:
        #     if i == 0:
        #         i = 1
        #         continue

        #     approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)


        #     M = cv2.moments(contour)
        #     if M['m00'] != 0.0:
        #         x = int(M['m10']/M['m00'])
        #         y = int(M['m01']/M['m00'])

        #     u, k = approx[0][0]

        #     if len(approx) == 4:
        #         cv2.drawContours(frame, [contour], 0, (0, 255, 0), 5)
        #         # cv2.putText(frame, "Rectangle", (u, k), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)

        # captured_image = Image.fromarray(frame)
        # photo_image = ImageTk.PhotoImage(image=captured_image)
        # self.videoLabel.photo_image = photo_image
        # self.videoLabel.configure(image=photo_image)
        # self.videoLabel.after(10, self.cam_loop)

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
            self.controls.move_to(90, 50, 30)
            time.sleep(0.5)
            self.controls.gripper_drop()
            time.sleep(0.5)
            self.controls.move_to(90, 50, 80)
            self.controls.move_to(80, 0, 80)

            # step 3
            self.controls.move_to(80, 0, 5)
            time.sleep(0.5)
            self.controls.gripper_pick()
            time.sleep(0.5)
            self.controls.move_to(80, 0, 80)
            self.controls.move_to(90, 50, 80)
            time.sleep(0.5)
            self.controls.move_to(90, 50, 60)
            time.sleep(0.5)
            self.controls.gripper_drop()
            time.sleep(0.5)
            self.controls.move_to(90, 50, 90)
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
