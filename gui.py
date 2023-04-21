import tkinter as tk
from slider import Slider
from robot import Robot

class GUI:
    process1Level = 0

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('500x300')
        self.__initWidgets()
        self.robot = Robot()
        self.window.mainloop()

    def bodyRotationWidgetCallback(self, value = 0):
        self.robot.bodyRotationServo.setAngle(self.bodyRotationSlider.get())

    def heightWidgetCallback(self, value=0):
        self.robot.heightServo.setAngle(self.heightSlider.get())

    def bodyRotationWidget(self):
        bodyRotationSliderLabel = tk.Label(self.window, text="Body Slider").grid(column=0,row=0)
        self.bodyRotationSlider = Slider(self.window, 0, 0, 180, self.bodyRotationWidgetCallback)
        self.bodyRotationSlider.returnWidget().grid(column=1,row=0)

    def heightWidget(self):
        heightSliderLabel = tk.Label(self.window, text="Height Slider").grid(column=0,row=1)
        self.heightSlider = Slider(self.window, 40, 40, 130, self.heightWidgetCallback)
        self.heightSlider.returnWidget().grid(column=1,row=1)

    def xCallback(self, value=20):
        self.robot.moveToXPosition(int(value))

    def xWidget(self):
        xLabel = tk.Label(self.window, text="X").grid(column=0,row=8)
        self.xSlider = Slider(self.window, 20, 0, 100, self.xCallback)
        self.xSlider.returnWidget().grid(column=1,row=8)

    def lengthWidgetCallback(self, value=0):
        self.robot.lengthServo.setAngle(self.lengthSlider.get())

    def lengthWidget(self):
        lengthSliderLabel = tk.Label(self.window, text="Length Slider").grid(column=0,row=4)
        self.lengthSlider = Slider(self.window, 110, 90, 180, self.lengthWidgetCallback)
        self.lengthSlider.returnWidget().grid(column=1,row=6)

    def posConveyorWidgetCallback(self, value=0):
        self.robot.moveToPosition(8, 3, 5.5)
        # self.robot.conveyorPickReady()

    def posConveyorWidget(self):
        button = tk.Button(self.window, text='Pick Ready', command=self.posConveyorWidgetCallback).grid(column=0,row=2)

    def posConveyorPickWidgetCallback(self, value=0):
        self.robot.conveyorPick()

    def posConveyorPickWidget(self):
        button = tk.Button(self.window, text='Pick', command=self.posConveyorPickWidgetCallback).grid(column=1,row=2)

    def posConveyorDropWidgetCallback(self, value=0):
        self.robot.conveyorDrop()

    def posConveyorDropWidget(self):
        button = tk.Button(self.window, text='Drop', command=self.posConveyorDropWidgetCallback).grid(column=2,row=2)

    def moveToAreaWidgetCallback(self, value=0):
        self.robot.moveToArea()

    def moveToAreaWidget(self):
        button = tk.Button(self.window, text='Area 1', command=self.moveToAreaWidgetCallback).grid(column=0,row=3)

    def moveToAreaDropWidgetCallback(self, value=0):
        self.robot.moveToAreaDrop()

    def moveToAreaDropWidget(self):
        button = tk.Button(self.window, text='Drop', command=self.moveToAreaDropWidgetCallback).grid(column=1,row=3)

    def moveToAreaPickWidgetCallback(self, value=0):
        self.robot.moveToAreaPick()

    def moveToAreaPickWidget(self):
        button = tk.Button(self.window, text='Pick', command=self.moveToAreaPickWidgetCallback).grid(column=2,row=3)

    def process1Callback(self, value=0):
        self.robot.process1(self.process1Level)
        self.process1Level += 1

    def process1Widget(self):
        button = tk.Button(self.window, text='Process 1', command=self.process1Callback).grid(column=0,row=4)

    def __initWidgets(self):
        self.bodyRotationWidget()
        self.heightWidget()
        self.posConveyorWidget()
        self.posConveyorPickWidget()
        self.posConveyorDropWidget()
        self.lengthWidget()
        self.moveToAreaWidget()
        self.moveToAreaDropWidget()
        self.moveToAreaPickWidget()
        self.process1Widget()
        self.xWidget()

    def close(self):
        self.robot.close()
        exit()
