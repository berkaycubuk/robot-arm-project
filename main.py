#!/usr/bin/python
from gui import GUI
import RPi.GPIO as GPIO

gui = GUI()
gui.close()

GPIO.cleanup()
