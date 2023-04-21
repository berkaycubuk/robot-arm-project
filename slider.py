import tkinter as tk

class Slider:
    def __init__(self, window, value, minValue, maxValue, commandFunc):
        self.widget = tk.Scale(window, from_=minValue, to=maxValue, orient=tk.HORIZONTAL, command=commandFunc)
        self.widget.set(value)
        #self.widget.pack()
        #return self.widget

    def returnWidget(self):
        return self.widget

    def get(self):
        return self.widget.get()

    def set(self, value):
        self.widget.set(value)
