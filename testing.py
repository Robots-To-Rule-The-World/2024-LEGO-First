from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
ready = hub.imu.ready()
while ready != True:
    ready = hub.imu.ready()
    print("waiting")
    wait(3)

# Eb Bb F Bb Eb Bb G Eb Bb

song = ["Eb5/8", "Bb4/8", "F5/8", "Bb4/8", "Eb5/8", "Bb4/16", "G5/16", "Eb5/8", "Bb4/8"]

hub.speaker.play_notes(song)