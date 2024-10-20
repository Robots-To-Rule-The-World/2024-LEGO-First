from hub import port, motion_sensor
import runloop, motor_pair, sys, motor, math, time

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE

wheel_diameter = 5.6 #cm

def degreesForDistance(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

#These functions work well with yaw correction
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

async def move_straight(distance, speed):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance),0,velocity=-1*speed)

async def main():
    # Reset Base 1, do not change these lines
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

    #put your code here, use
    # spin_turn_cw(degrees to turn, speed) to turn clockwise or right
    # sping_turn_ccw(degrees to turn, speed) to turn counter clockwise or left
    # move_straight_corrected(distance, speed) to go straight with some correction, good for long straights
    # note - don't change the speed after you have set your distance! changing the speed will affect your distance 

    #Example:
    #await move_straight_corrected(15,500) # (distance, speed) distance is arbitrary, must figure out by experimenation
                                          # speed can be fast, but if you change speed it will affect distance, choose speed first
    #await spin_turn_cw(45,200)
    #await move_straight_corrected(16,300)

    sys.exit(0)

runloop.run(main())
