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

# song = ["Eb5/8", "Bb4/8", "F5/8", "Bb4/8", "Eb5/8", "Bb4/8", "G5/16", "Eb5/16", "Bb4/8"]
# song = ["Eb5/8", "F5/8", "Eb5/8", "F5/8", "Eb5/8", "F5/8", "Eb5/8", "F5/8", "Eb5/8", "F5/8"]
# hub.speaker.play_notes(song)

#motor definition, ports C&D cuz that's how we roll
motor_left_C = Motor(Port.C,Direction.COUNTERCLOCKWISE)
motor_right_D = Motor(Port.D,Direction.CLOCKWISE)
    
#need distance between wheel touching surface in mm
b = DriveBase(motor_left_C, motor_right_D, 87, 110)
# b.use_gyro(True)
state = b.state()
print(state)

async def Run():
    b.settings(400)
    await b.straight(140, Stop.HOLD, True)
    await b.turn(-40, Stop.HOLD, True)
    await b.straight(400, Stop.HOLD, True) #gets first krill
    await b.turn(45, Stop.HOLD, True)
    await b.straight(200, Stop.HOLD, True) #gets second krill
    await b.turn(40, Stop.HOLD, True)
    await b.straight(110, Stop.HOLD, True) #gets second krill
    # b.settings(400, 0, 200, 200)
    await b.turn(-150, Stop.HOLD, True)
    await b.straight(110, Stop.HOLD, True)
    await b.straight(1200, Stop.HOLD, True)
    await b.turn(-90, Stop.Hold, True)
run_task(Run())