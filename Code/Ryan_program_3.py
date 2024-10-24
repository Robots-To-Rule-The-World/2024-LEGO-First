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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance),0,velocity=1*speed)

async def open_claw():
    await motor.run_to_absolute_position(port.B,300,500)

async def close_claw():
    await motor.run_to_absolute_position(port.B,300,500)

async def main():
    # Reset Base 1, do not change these lines
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
    motion_sensor.reset_yaw(0)
    #await runloop.until(motion_sensor.stable)

    #put your code here, use
    # await spin_turn_cw(degrees to turn, speed) to turn clockwise or right
    # await spin_turn_ccw(degrees to turn, speed) to turn counter clockwise or left
    # await move_straight(distance in cm, speed) to go straight, you can use a negative speed to go backwards

    #Example:
    #await move_straight(45,500)
    #await spin_turn_cw(45,200)
    #await move_straight_corrected(16,300)


    await move_straight(15,-900)
    await spin_turn_cw(75,600)
    await move_straight(67,-900)
    await spin_turn_ccw(55,600)
    await move_straight(10,-900)

    await open_claw()
    await spin_turn_ccw(10,600)
    await spin_turn_cw(10,600)
    await spin_turn_ccw(10,600)
    await spin_turn_cw(10,600)
    await spin_turn_ccw(10,600)
    await spin_turn_cw(10,600)
    await move_straight(10,900)
    await close_claw()

    await spin_turn_cw(35,600)
    await move_straight(30,-900)
    await spin_turn_cw(35,600)
    await move_straight(55,-1200)
    
    await move_straight(5,-500)

    sys.exit(0)

runloop.run(main())
