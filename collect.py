#!/usr/bin/python
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from servo import Servo
import tkinter as tk
import time
import csv

pwm = PCA9685()
pwm.setPWMFreq(50)

bodyServo = Servo(pwm, 0, 70)
leftServo = Servo(pwm, 1, 90)
rightServo = Servo(pwm, 2, 120)
gripServo = Servo(pwm, 3, 150)

window = tk.Tk()
window.geometry('500x300')

def saveCommand():
    bodyServo.setAngle(int(bodyInput.get()), True)
    leftServo.setAngle(int(leftInput.get()), True)
    rightServo.setAngle(int(rightInput.get()), True)

def writeCommand():
    f = open('./data.csv', 'a')
    writer = csv.writer(f)
    writer.writerow([
        int(bodyInput.get()), 
        int(leftInput.get()),
        int(rightInput.get()),
        float(xInput.get()),
        float(yInput.get()),
        float(zInput.get()),
    ])
    f.close()

tk.Label(window, text="Body").grid(row=0, column=0)
bodyInput = tk.Entry(window, width=15)
bodyInput.insert(tk.END, str(bodyServo.getAngle()))
bodyInput.grid(row=1, column=0)

tk.Label(window, text="Left").grid(row=2, column=0)
leftInput = tk.Entry(window, width=15)
leftInput.insert(tk.END, str(leftServo.getAngle()))
leftInput.grid(row=3, column=0)

tk.Label(window, text="Right").grid(row=4, column=0)
rightInput = tk.Entry(window, width=15)
rightInput.insert(tk.END, str(rightServo.getAngle()))
rightInput.grid(row=5, column=0)

tk.Label(window, text="X position").grid(row=0, column=1)
xInput = tk.Entry(window, width=15)
xInput.grid(row=1, column=1)

tk.Label(window, text="Y position").grid(row=2, column=1)
yInput = tk.Entry(window, width=15)
yInput.grid(row=3, column=1)

tk.Label(window, text="Z position").grid(row=4, column=1)
zInput = tk.Entry(window, width=15)
zInput.grid(row=5, column=1)

tk.Button(window, text="Move to positions", command=saveCommand).grid(row=6, column=0)

tk.Button(window, text="Save Values", command=writeCommand).grid(row=6, column=1)

window.mainloop()

pwm.exit_PCA9685()
GPIO.cleanup()
