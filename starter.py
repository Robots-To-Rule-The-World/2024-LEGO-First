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
    b = DriveBase(motor_left_C, motor_right_D, WHEEL_DIAMETER, DRIVER_BASE)
    return (hub, b)

hub, bot = InitializeRobot()
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



async def Run():
    await b.straight(100, Stop.BRAKE, True)
    await b.turn(-45, Stop.HOLD, True)
    await b.straight(350, Stop.BRAKE, True)

run_task(Run())