import os
import sys
import time

from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.button import Button

class Robot:
    def __init__(self, tank: MoveDifferential, touchSensor: TouchSensor, eye: InfraredSensor):
        self.tank = tank
        self.touchSensor = touchSensor
        self.botton = Button()
        self.eye = eye

    def randomWalk(self):
        if self.touchSensor.is_pressed:
            self.tank.off()
            self.tank.turn_degrees(speed = 30, degrees = 180)
            self.tank.on(left_speed = 20, right_speed = 20)
        else:
            self.tank.on(left_speed = 45, right_speed = 45)

    def findBeanDirection(self):
        distance = self.eye.distance(channel=1)
        direction = self.eye.heading(channel=1)
        print("Distance {} Direct {}".format(distance, direction))
        self.tank.turn_degrees(speed = 10, degrees = 10)

