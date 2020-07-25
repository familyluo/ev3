#!/usr/bin/env micropython
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
import random

from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.button import Button
from robot import Robot


# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def randomWalk(tank: MoveDifferential, touchSensor: TouchSensor):
    btn = Button()
    while not btn.any():
        if touchSensor.is_pressed:
            tank.off()
        else:
            tank.on(left_speed = 45, right_speed = 45)


def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    print('How are you?')
    print("")
    print("Hello Selina.")
    print("Hello Ethan.")
    STUD_MM = 8
    tank = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)
    motorLift = MediumMotor(OUTPUT_D)
    sound = Sound()

    # sound.speak('How are you master!')
   # sound.speak("I like my family")
   # sound.speak("I like my sister and i like my brother.")
    sound.beep()

    eye = InfraredSensor(INPUT_1)
    robot = Robot(tank, None, eye)
    botton = Button()
    while not botton.any():
        distance = eye.distance(channel=1)
        heading = eye.heading(channel=1)
        print('distance: {}, heading: {}'.format(distance, heading))

        motorLift.on_to_position(speed=40, position=-7200, block=True)  #20 Rounds

        if distance is None:
            sound.speak("I am lost, there is no beacon!")
        else:
            if (distance < 14):
                tank.off()
                sound.speak("I am very close to the beacon!")
                motorLift.on_to_position(speed=40, position=7200, block=True)
                sound.speak("I had to get some more rubbish.")
                sound.speak("Please wait while I lift up my fork.")
                tank.turn_right(speed=20, degrees=random.randint(290, 340))  # random.randint(150, 210)
                tank.on_for_seconds(left_speed=20, right_speed=20, seconds=20)
                tank.turn_right(speed=20, degrees=330)
                motorLift.on_to_position(speed=40, position=0, block=True)

            elif distance >= 100:
                sound.speak("I am too faraway from the beacon")
            elif (distance  < 99) and (-4 <= heading <= 4):  # in right heading
                sound.speak("Moving farward")
                tank.on(left_speed=20, right_speed=20)
            else:
                if heading > 0:
                    tank.turn_left(speed=20, degrees=20)
                else:
                    tank.turn_right(speed=20, degrees=20)
                sound.speak("I am finding the beacon.")


        time.sleep(0.1)

if __name__ == '__main__':
    main()
