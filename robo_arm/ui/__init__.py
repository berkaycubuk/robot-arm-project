import tkinter as tk
from tkinter import ttk
import time
from robo_arm.controls import Controls
from robo_arm.camera import Camera
import cv2
from PIL import Image, ImageTk
import numpy as np
import yaml

def load_blocks_file():
    with open(r'/home/jnuu/robot-arm/blocks.yaml') as file:
        blocks_file = yaml.safe_load(file)

    return blocks_file['blocks']

def write_blocks_file(data):
    with open(r'/home/jnuu/robot-arm/blocks.yaml', 'w') as file:
        yaml.dump({'blocks': data}, file)

def load_orders_file():
    with open(r'/home/jnuu/robot-arm/orders.yaml') as file:
        orders_file = yaml.safe_load(file)

    return orders_file

def write_orders_file(data):
    with open(r'/home/jnuu/robot-arm/orders.yaml', 'w') as file:
        yaml.dump(data, file)

def find_order(orders, order_id):
    found = None
    for order in orders:
        if order['id'] == order_id:
            found = order
            break

    return found

def find_block(blocks, block_name):
    found = None
    for block in blocks:
        if block['name'] == block_name:
            found = block
            break

    return found

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
        orders_page = OrdersPage(self, frame2).grid(row=0,column=0)
        notebook.add(frame2, text='Görevler')

        frame3 = tk.Frame(notebook)
        blocks_page = BlocksPage(self, frame3).grid(row=0,column=0)
        notebook.add(frame3, text='Bloklar')

        notebook.enable_traversal()

class OrdersPage(tk.Frame):
    def __init__(self, root, container):
        super().__init__(container)

        orders = []

        orders = load_orders_file()

        orders_listbox = tk.Listbox(self)
        orders_listbox.grid(row=0,column=0)

        order_details = tk.Frame(self)
        order_details.grid(row=0,column=1)

        for order in orders:
            orders_listbox.insert(tk.END, order['id'])

        block_names = []
        for block in load_blocks_file():
            block_names.append(block['name'])

        order_id_label = tk.Label(order_details, text="ID:").grid(row=0,column=0)
        order_id_value = tk.Label(order_details, text="")
        order_id_value.grid(row=0,column=1)

        order_action_label = tk.Label(order_details, text="Aksiyon:").grid(row=1,column=0)
        order_action_value = tk.Label(order_details, text="")
        order_action_value.grid(row=1,column=1)

        def order_click_callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                order = find_order(orders, data)
                order_id_value.configure(text=order['id'])
                order_action_value.configure(text=order['action'])

        orders_listbox.bind("<<ListboxSelect>>", order_click_callback)

        x_input_label = tk.Label(self, text="x konumu").grid(row=1,column=0)
        x_value = tk.StringVar()
        x_input = tk.Entry(self, textvariable=x_value).grid(row=1,column=1)

        y_input_label = tk.Label(self, text="y konumu").grid(row=2,column=0)
        y_value = tk.StringVar()
        y_input = tk.Entry(self, textvariable=y_value).grid(row=2,column=1)

        block_input_label = tk.Label(self, text="blok").grid(row=3,column=0)
        block_value = tk.StringVar()
        block_input = ttk.Combobox(self, textvariable=block_value)
        block_input['values'] = tuple(block_names)
        block_input.grid(row=3,column=1)

class BlocksPage(tk.Frame):
    def __init__(self, root, container):
        super().__init__(container)

        blocks = []

        blocks = load_blocks_file()

        blocks_listbox = tk.Listbox(self)
        blocks_listbox.grid(row=0,column=0)

        for block in blocks:
            blocks_listbox.insert(tk.END, block['name'])

        form = tk.Frame(self)
        form.grid(row=0, column=1)

        add_block_name_label = tk.Label(form, text="Blok adı").grid(row=0,column=1)
        block_name = tk.StringVar()
        add_block_name = tk.Entry(form, textvariable=block_name).grid(row=0, column=2)
        block_x = tk.StringVar()
        add_block_x_label = tk.Label(form, text="x konumu").grid(row=1,column=1)
        add_block_x = tk.Entry(form, textvariable=block_x).grid(row=1, column=2)
        block_y = tk.StringVar()
        add_block_y_label = tk.Label(form, text="y konumu").grid(row=2,column=1)
        add_block_y = tk.Entry(form, textvariable=block_y).grid(row=2, column=2)
        block_level = tk.StringVar()
        add_block_level_label = tk.Label(form, text="blok seviyesi").grid(row=3,column=1)
        add_block_level = tk.Entry(form, textvariable=block_level).grid(row=3, column=2)
        block_color = tk.StringVar()
        add_block_color_label = tk.Label(form, text="blok rengi").grid(row=4,column=1)
        add_block_color = ttk.Combobox(form, textvariable=block_color)
        add_block_color['values'] = ('Kırmızı', 'Beyaz')
        add_block_color.grid(row=4, column=2)

        def add_block():
            blocks.append({
                'name': block_name.get(),
                'x': block_x.get(),
                'y': block_y.get(),
                'level': block_level.get(),
                'color': block_color.get()
            })
            blocks_listbox.insert(tk.END, block_name.get())
            write_blocks_file(blocks)
        add_block_button = tk.Button(form, text="blok ekle", command=add_block).grid(row=5,column=1)

        def delete_block():
            if blocks_listbox.curselection() is None:
                return
            for item in blocks:
                if blocks_listbox.get(blocks_listbox.curselection()[0]) == item['name']:
                    blocks.remove(item)
            blocks_listbox.delete(blocks_listbox.curselection()[0])
            write_blocks_file(blocks)
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

        def exec_order(order):
            blocks = load_blocks_file()
            if order['action'] == "pick":
                block = find_block(blocks, order['block']) 
                if block is None:
                    print("blok bulunamadı")
                    return
                self.controls.move_to(int(block['x']), int(block['y']), 80)
                if int(block['level']) == 0:
                    self.controls.move_to(int(block['x']), int(block['y']), 10)
                else:
                    self.controls.move_to(int(block['x']), int(block['y']), int(block['level']) * 25)
                self.controls.gripper_pick()
                self.controls.move_to(int(block['x']), int(block['y']), 80)
            elif order['action'] == "drop":
                self.controls.move_to(int(order['to_x']), int(order['to_y']), 80)
                if int(order['to_level']) == 0:
                    self.controls.move_to(int(order['to_x']), int(order['to_y']), 10)
                else:
                    self.controls.move_to(int(order['to_x']), int(order['to_y']), int(order['to_level']) * 25)
                self.controls.gripper_drop()
                self.controls.move_to(int(order['to_x']), int(order['to_y']), 80)

                for key, block in enumerate(blocks):
                    if block['name'] == order['block']:
                        blocks[key]['x'] = order['to_x']
                        blocks[key]['y'] = order['to_y']
                        blocks[key]['level'] = order['to_level']

                write_blocks_file(blocks)

        def execute_orders():
            orders = load_orders_file()

            for order in orders:
                exec_order(order)
                time.sleep(0.5)

        button_exec_orders = tk.Button(
                left_controls_frame, text="Görevleri Çalıştır", command=execute_orders)
        button_exec_orders.grid(row=3, column=0, ipadx=30, ipady=20)

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
