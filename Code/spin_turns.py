from hub import port, motion_sensor
import runloop, motor_pair, sys

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5

# default speed (reducing parameter input until we know wth is up)
DEFAULT_SPEED = 100

async def spin_turn_cw(degrees):
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degrees*2, 1000, -1000)
    return

async def spin_turn_ccw(degrees):
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degrees*2, -1000, 1000)
    return

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
    await spin_turn_cw(180) # in degrees
    await spin_turn_ccw(360)
    return

runloop.run(main())