from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

TIME_SECOND = 1000

hub = PrimeHub()
ready = hub.imu.ready()
while ready != True:
    ready = hub.imu.ready()
    print("waiting")
    wait(3)

#motor definition, ports C&D cuz that's how we roll
motor_left_C = Motor(Port.C,Direction.COUNTERCLOCKWISE)
motor_right_D = Motor(Port.D,Direction.CLOCKWISE)
    
#need distance between wheel touching surface in mm
b = DriveBase(motor_left_C, motor_right_D, 87, 110)
state = b.state()

    
"""
                    -
                    .
                    -
                    .
                    -
                    .
               ^    -
|....|....|....|....| (table edge)
"""

async def Run():
    sw = StopWatch()
    b.settings(400)
    await b.straight(140, Stop.HOLD, True)
    await b.turn(-48, Stop.HOLD, True)
    await b.straight(370, Stop.HOLD, True) # get squid
    await b.straight(-100, Stop.HOLD, True) 
    await b.turn(60, Stop.HOLD, True)
    await b.straight(280, Stop.HOLD, True)
    await b.turn(-80, Stop.HOLD, True)
    await b.straight(460, Stop.HOLD, True)
    # # begin Anglerfish
    await b.turn(-45, Stop.HOLD, True) # turn towards anglerfish
    await b.straight(130, Stop.HOLD, True) # engage the switch (changed from 175)
    b.settings(100)
    await b.turn(45, Stop.HOLD, True)
    b.settings(400)
    await b.straight(270, Stop.HOLD, True) # this should stop once the fish is hiding
    

    await b.turn(-25, Stop.HOLD, True)
    await b.straight(400, Stop.HOLD, True)
    await b.turn(-75, Stop.HOLD, True)
    await b.straight(800, Stop.HOLD, True)
    sw.pause()
    end = sw.time()
    print("run took {} seconds".format(end))
run_task(Run())

"""_summary_
create a function that stores the inverse of the given function so you can review back to the original

program 2 and 4 are on laptop 4
"""