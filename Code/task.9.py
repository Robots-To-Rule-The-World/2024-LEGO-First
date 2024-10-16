from hub import port, motion_sensor
import runloop, motor, motor_pair, sys

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE


TURN_SPEED = 35
VELOCITY = 500
CAGE_HEIGHT = 60

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

async def lift_cage():
    await motor.run_for_degrees(port.A, -1*50, CAGE_HEIGHT)

async def lower_cage():
    await motor.run_for_degrees(port.A, 50, CAGE_HEIGHT)

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

    # hit the squid
    await move_straight_forward(39)

    # step awaaaaaay from the tower
    await move__straight_backward(15)

    # move to squid dropoff
    await spin_turn_ccw(35, TURN_SPEED)
    await move_straight_forward(30)
    await spin_turn_cw(50, TURN_SPEED)
    await move_straight_forward(30)

    # drop off the squid
    await lift_cage()
    await move__straight_backward(15)
    await lower_cage()

    # get back
    await move__straight_backward(20)
    await spin_turn_ccw(35, TURN_SPEED)
    await move__straight_backward(55)

    # await spin_turn_cw(90,150) # in degrees
    # await move_straight(10)
    #await spin_turn_ccw(90,150) # in degrees
    sys.exit(0)

runloop.run(main())
