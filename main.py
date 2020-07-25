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

    # print something to the screen of the device
    print('Hello World!')

    print('How are you?')
    print("")
    print("Hello selina.")
    print("Hello ethan.")
    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')
    print("I like my family")

    # leds = Leds()
    # leds.set_color('LEFT', 'ORANGE')
    # leds.set_color('RIGHT', 'RED')
    STUD_MM = 8
    tank = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)
    motorLift = MediumMotor(OUTPUT_D)
    sound = Sound()
    #sound.speak('Welcome to the E V 3 dev project!')

    # sound.speak('How are you master!')
   # sound.speak("I like my family")
   # sound.speak("I like my sister and i like my brother.")
    sound.beep()


    eye = InfraredSensor(INPUT_1)
    # touchSensor = TouchSensor(INPUT_2)
    robot = Robot(tank, None, eye)
    botton = Button()
    while not botton.any():
        # robot.randomWalk()
        # robot.findBeanDirection()
        distance = eye.distance(channel=1)
        heading = eye.heading(channel=1)
        print('distance: {}, heading: {}'.format(distance, heading))

        motorLift.on_to_position(speed=40, position=-7200, block=True)

        if distance is None:
            sound.speak("I am lost, there is no beacon!")
        else:
            if (distance < 14):
                tank.off()
                sound.speak("I am very close to the beacon!")
                # motorLift.on_for_seconds(speed=40, seconds=3)
                motorLift.on_to_position(speed=40, position=7200, block=True)
                sound.speak("I had to get some more rubbish.")
                sound.speak("Please wait while I lift up my fork.")
                tank.turn_right(speed=20, degrees=random.randint(290, 340))  # random.randint(150, 210)
                tank.on_for_seconds(left_speed=20, right_speed=20, seconds=20)
                tank.turn_right(speed=20, degrees=330)
                motorLift.on_to_position(speed=40, position=0, block=True)
                # finishLooking = False
                # while (not botton.any() and not finishLooking):
                #     tank.on(left_speed=20, right_speed=20)
                #     proximity = eye.proximity
                #     print('proximity: {}'.format(proximity))
                #     if proximity < 30:
                #         tank.off()
                #         sound.speak("I am too close to a obstacle, finding beacon")
                #         finishLooking = True

            elif distance >= 100:
                sound.speak("I am too faraway from the beacon")
            elif (distance  < 99) and (-4 <= heading <= 4):  # in right heading
                sound.speak("Moving farward")
                tank.on(left_speed=20, right_speed=20)
            else:
                # tank.off()
                if heading > 0:
                    tank.turn_left(speed=20, degrees=20)
                else:
                    tank.turn_right(speed=20, degrees=20)
                sound.speak("I am finding the beacon.")


        time.sleep(0.1)

    # Rotate 90 degrees clockwise
    # tank.turn_right(SpeedRPM(40), 90)

    # # Drive forward 500 mm
    # tank.on_for_distance(SpeedRPM(40), 500)

    # # Drive in arc to the right along an imaginary circle of radius 150 mm.
    # # Drive for 700 mm around this imaginary circle.
    # tank.on_arc_right(SpeedRPM(80), 150, 700)

    # Enable odometry
    # tank.odometry_start()

    # # Use odometry to drive to specific coordinates
    # tank.on_to_coordinates(SpeedRPM(40), 300, 300)

    # # Use odometry to go back to where we started
    # tank.on_to_coordinates(SpeedRPM(40), 0, 0)

    # # Use odometry to rotate in place to 90 degrees
    # tank.turn_to_angle(SpeedRPM(40), 90)

    # # Disable odometry
    # tank.odometry_stop()

    # leftMotor = LargeMotor()
    # leftMotor.on_for_seconds(speed = 50, seconds=3)

    # leftMotor.on_for_degrees(speed=80, degrees=90, brake=True, block=True)


    # wait a bit so you have time to look at the display before the program
    # exits
    # time.sleep(5)

if __name__ == '__main__':
    main()
