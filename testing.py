from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

hub = PrimeHub()
ready = hub.imu.ready()
while ready != True:
    ready = hub.imu.ready()
    print("waiting")
    wait(3)

song = ["Eb5/8", "Bb4/8", "F5/8", "Bb4/8", "Eb5/8", "Bb4/8", "G5/16", "Eb5/16", "Bb4/8"]
# song = ["Eb5/8", "Bb4/8"]

#motor definition, ports C&D cuz that's how we roll
motor_left_C = Motor(Port.C,Direction.COUNTERCLOCKWISE)
motor_right_D = Motor(Port.D,Direction.CLOCKWISE)
    
#need distance between wheel touching surface in mm
b = DriveBase(motor_left_C, motor_right_D,81.6,110)
b.use_gyro(True)
state = b.state
print(state)

spinny = Motor(Port.E, Direction.CLOCKWISE)

async def play_song():
    await hub.speaker.play_notes(song)

async def move_spinny():
    await spinny.run_time(1000, 2000, Stop.HOLD)

async def main():
    await multitask(play_song(), move_spinny(), b.straight(1000))

run_task(main())