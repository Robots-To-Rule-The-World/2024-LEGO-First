from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

TIME_SECOND = 1000
WHEEL_DIAMETER = 87
DRIVER_BASE = 110

"""
**********************
**********************
**********************
**********************
DO NOT EDIT THIS BLOCK
**********************
**********************
**********************
**********************
"""
def InitializeRobot():
    hub = PrimeHub()
    ready = hub.imu.ready()
    while ready != True:
        ready = hub.imu.ready()
        print("waiting")
        wait(3)    

    motor_left_C = Motor(Port.C,Direction.COUNTERCLOCKWISE)
    motor_right_D = Motor(Port.D,Direction.CLOCKWISE)
    bot = DriveBase(motor_left_C, motor_right_D, WHEEL_DIAMETER, DRIVER_BASE)
    return (hub, bot)

def InitializeMotors():
    front_motor = Motor(Port.A, Direction.CLOCKWISE)
    rear_motor = Motor(Port.B, Direction.CLOCKWISE)
    return front_motor, rear_motor

hub, bot = InitializeRobot()
front, pinchy = InitializeMotors()
"""
^^^^^^^^^^^^^^^^^^^^^^
**********************
**********************
**********************
**********************
DO NOT EDIT THIS BLOCK
**********************
**********************
**********************
**********************
"""

"""
HOW TO MOVE THE ROBOT:

The Drivebase (bot) is how you will move the robot. Here are some useful functions:

"straight" 
 - distance in mm
 - the method of stopping Stop.HOLD, Stop.BRAKE, Stop.COAST
 - whether you want to have the function be awaitable
bot.straight(100, Stop.BRAKE, True)

"turn" 
 - degrees from -180 to 180. Negative numbers turn left, positive turn right
 - the method of stopping Stop.HOLD, Stop.BRAKE, Stop.COAST
 - whether you want to have the function be awaitable
bot.turn(-45, Stop.HOLD, True)

Radial Turns
You can perform a radial turn by using the "drive" function

Backwards
you can make the robot go backwards by passing in a negative distance (i hope)

Perform Actions while Moving (Concurrent robot commands)
For this you will need to use async functions:

async def func1():
    await bot.turn

async def func2():
    await bot.turn(-45, Stop.HOLD, True)

async def main():
    await multitask(func1(), func2(), bot.straight(1000, Stop.BRAKE, True))

    
to use the front motor, utilize the "front" motor:
await front.run_time(1000, 2000, Stop.HOLD)

to utilize the pinchers in the back, use the "pinchy" motor:
await pinchy.run_time(1000, 2000, Stop.HOLD)

"""

##########################
# INSERT YOUR CODE BELOW #
##########################
song = ["Eb5/8", "Bb4/8", "F5/8", "Bb4/8", "Eb5/8", "Bb4/8", "G5/16", "Eb5/16", "Bb4/8"]
hub.speaker.play_notes(song)

# forward
bot.straight(100, Stop.BRAKE)
# backward
bot.straight(-100, Stop.BRAKE)


# LET'S GOOOOOOOOOOOOOOOOO