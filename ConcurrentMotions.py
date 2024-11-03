
"""
This example shows how to run multiple concurrent actions at once

Author: @nvcexploder
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task



"""
The Scenario: 

Let's say we want to have a robot do multiple things at the same time 
without waiting? For example: I want to move forward, activate 
another motor, and play a song at the same time? 

The answer is in the pybricks.tools library, with a function called `multitask`

Let's get started!
"""

# this is out hub definition, followed by our bot drive_base inintialization
hub = PrimeHub()
left = Motor(Port.C,Direction.COUNTERCLOCKWISE)
right = Motor(Port.D)
b = DriveBase(left, right, 81.6, 110)
b.use_gyro(True)

# our stopwatch tells us how long each function takes
sw = StopWatch()

# spinny is our extra motor
spinny = Motor(Port.E, Direction.CLOCKWISE)

# song is a great song to listen to Today
song = ["Eb5/8", "Bb4/8", "F5/8", "Bb4/8", "Eb5/8", "Bb4/8", "G5/16", "Eb5/16", "Bb4/8"]

async def play_song():
    """
    play_song defines a song, and then plays it for us
    """
    await hub.speaker.play_notes(song)

async def move_spinny():
    """
    move_spinny defines then rotates another motor somewhere on the hub
    """
    await spinny.run_time(1000, 2000, Stop.HOLD)

async def sequential():
    """
    sequential executes the same three tasks sequentially 
    """
    await play_song()
    await move_spinny()
    await b.straight(1000)
    end = sw.time()
    

async def main():
    """
    main executes 3 tasks simultaneously via the multitask function
    """
    await multitask(play_song(), move_spinny(), b.straight(1000))

# initialize our timer    
sw.pause()
sw.reset()
sw.resume()
# run the sequential task
run_task(sequential())
#stop the clock and get the time
sw.pause()
end = sw.time()
print("sequential took {} seconds".format(end))

# initialize the timer again
sw.reset()
sw.resume()
# run our sequential task
run_task(main())
# stop the clock and get the time
end = sw.time()
print("main took {} seconds".format(end))

async def CANT_STOP_WONT_STOP(length, funk, *args):
    ready = hub.imu.ready()
    bouncer = StopWatch()
    await funk(args)
    while ready != True:
        ready = hub.imu.ready()
        bounce = bouncer.time()
        if bounce > length:
            break

    # await     while ready != True:
    #     ready = hub.imu.ready()
    #     print("waiting")
    #     wait(3)   
    # bouncer = StopWatch()
    # bounce = bouncer.time()
    # while bounce < length:
            
