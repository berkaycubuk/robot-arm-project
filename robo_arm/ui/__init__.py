import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from robo_arm.controls import Controls
from robo_arm.camera import Camera
import cv2
from PIL import Image, ImageTk
import numpy as np
import yaml
import random
import string
from concurrent import futures
from robo_arm.utils import load_blocks_file, write_blocks_file, load_orders_file, write_orders_file, find_order, find_block

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

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

        def delete_order():
            selection = orders_listbox.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                for order in orders:
                    if data == order['id']:
                        orders.remove(order)
                orders_listbox.delete(index)
                write_orders_file(orders)
            else:
                messagebox.showerror('HATA', 'Silmek için herhangi bir görev seçmediniz.')

        delete_button = tk.Button(order_details, text="Sil", command=delete_order).grid(row=2,column=0)

        def order_click_callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                order = find_order(orders, data)
                order_id_value.configure(text=order['id'])
                order_action_value.configure(text=order['action'])

        orders_listbox.bind("<<ListboxSelect>>", order_click_callback)

        name_input_label = tk.Label(self, text="").grid(row=1,column=0)
        name_value = tk.StringVar()
        name_input = tk.Entry(self, textvariable=name_value).grid(row=1,column=1)

        x_input_label = tk.Label(self, text="x konumu").grid(row=2,column=0)
        x_value = tk.StringVar()
        x_input = tk.Entry(self, textvariable=x_value).grid(row=2,column=1)

        y_input_label = tk.Label(self, text="y konumu").grid(row=3,column=0)
        y_value = tk.StringVar()
        y_input = tk.Entry(self, textvariable=y_value).grid(row=3,column=1)

        level_input_label = tk.Label(self, text="seviye").grid(row=4,column=0)
        level_value = tk.StringVar()
        level_input = tk.Entry(self, textvariable=level_value).grid(row=4,column=1)

        block_input_label = tk.Label(self, text="blok").grid(row=5,column=0)
        block_value = tk.StringVar()
        block_input = ttk.Combobox(self, textvariable=block_value)
        block_input['values'] = tuple(block_names)
        block_input.grid(row=5,column=1)

        action_input_label = tk.Label(self, text="aksiyon").grid(row=6,column=0)
        action_value = tk.StringVar()
        action_input = ttk.Combobox(self, textvariable=action_value)
        action_input['values'] = ('pick', 'drop')
        action_input.grid(row=6,column=1)

        def add_order():
            #validation
            if name_value.get() == "":
                return

            random_id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            orders.append({
                'id': name_value.get(),
                'action': action_value.get(),
                'block': block_value.get(),
                'to_x': x_value.get(),
                'to_y': y_value.get(),
                'to_level': level_value.get()
            })
            write_orders_file(orders)
        tk.Button(self, text="Ekle", command=add_order).grid(row=7,column=0)

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
            # validation
            if block_name.get() == "":
                return

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

        self.red_lower = np.array([100 + 50,100,100], dtype='uint8')
        self.red_upper = np.array([255 - 50,255,255], dtype="uint8")

        self.white_lower = np.array([0,0,255 - 50], dtype="uint8")
        self.white_upper = np.array([255,50,255], dtype="uint8")

        self.filter_coordinates = [200,120,540,340]

        self.videoLabel = tk.Label(self)
        self.videoLabel.grid(row=0, column=1)
        self.cam_loop()

        self.right_controls().grid(row=0, column=2)

    def cam_loop(self):
        frame = self.camera.read()
        cropped_frame = frame[120:340,200:540]

        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            length = abs(x2 - x1)
            height = abs(y2 - y1)
            if length >= 40 and height >= 40:
                cv2.rectangle(frame, (x1 + self.filter_coordinates[0], y1 + self.filter_coordinates[1]), (x2 + self.filter_coordinates[0], y2 + self.filter_coordinates[1]), (0, 0, 255), 5)

        # white
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.white_lower, self.white_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            length = abs(x2 - x1)
            height = abs(y2 - y1)
            if length >= 40 and height >= 40:
                cv2.rectangle(frame, (x1 + self.filter_coordinates[0], y1 + self.filter_coordinates[1]), (x2 + self.filter_coordinates[0], y2 + self.filter_coordinates[1]), (255, 255, 255), 5)

        rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        tk_image = self.camera.tk_image(rgba)
        self.videoLabel.photo_image = tk_image
        self.videoLabel.configure(image=tk_image)
        self.videoLabel.after(10, self.cam_loop)

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

        def execute_orders_callback():
            thread_pool_executor.submit(execute_orders)

        def execute_orders():
            orders = load_orders_file()
            success = True

            for order in orders:
                status, message = self.controls.exec_order(order, self.camera)
                if status == 'error':
                    success = False
                    messagebox.showerror('HATA', message)
                    break

                time.sleep(0.5)

            if success:
                messagebox.showinfo('Tamamlandı', 'Görevler başarıyla tamamlandı!')

        button_exec_orders = tk.Button(
                left_controls_frame, text="Görevleri Çalıştır", command=execute_orders_callback)
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
