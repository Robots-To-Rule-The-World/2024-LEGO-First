from hub import port, motion_sensor
import runloop, motor_pair, sys

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE

# Globals for directional motion and turn speed
TURN_SPEED = 35
VELOCITY = 500

def degreesForDistance(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

async def spin_turn_cw(degrees,speed):
    motion_sensor.reset_yaw(0)
    motor_pair.move_tank(motor_pair.PAIR_1, speed,-1*speed)
    while abs(motion_sensor.tilt_angles()[0]*.1) < degrees:
        dummy = 1
    motor_pair.stop(motor_pair.PAIR_1)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(0.1), 0)

async def spin_turn_ccw(degrees,speed):
    motion_sensor.reset_yaw(0)
    motor_pair.move_tank(motor_pair.PAIR_1, -1*speed,speed)
    while abs(motion_sensor.tilt_angles()[0]*.1) < degrees:
        dummy = 1
    motor_pair.stop(motor_pair.PAIR_1)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(0.1), 0)

async def move_straight_forward(distance):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -1*degreesForDistance(distance), 0, velocity=VELOCITY)
    #this is uncorrected, we need a corrective straight function as wheels are getting caught on the board

async def move__straight_backward(distance):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance), 0, velocity=VELOCITY)
    #this is uncorrected, we need a corrective straight function as wheels are getting caught on the board

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    await move_straight(50)
    await spin_turn_cw(90,150) # in degrees
    await move_straight(10)
    #await spin_turn_ccw(90,150) # in degrees
    sys.exit(0)

runloop.run(main())
