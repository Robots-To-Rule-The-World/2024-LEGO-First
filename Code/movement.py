from hub import port, motion_sensor
import runloop, motor_pair, sys

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE
desired_degree = 0

def degreesForDistance(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

# Function that returns true when the absolute yaw angle reaches desired degree
def turn_done():
    # convert tuple decidegree into same format as in app and blocks
    global desired_degrees
    print(motion_sensor.tilt_angles()[0])
    return abs(motion_sensor.tilt_angles()[0] * -0.1) > desired_degrees


async def pivot_turn_cw(degrees,speed,steering):    
    global desired_degrees
    desired_degrees = degrees
    # move with a steering of 50
    motor_pair.move(motor_pair.PAIR_1, steering, velocity=speed)
    await runloop.until(turn_done)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    motor_pair.stop(motor_pair.PAIR_1)

async def pivot_turn_ccw(degrees,speed,steering):
    global desired_degrees
    desired_degrees = degrees
    # move with a steering of 50
    motor_pair.move(motor_pair.PAIR_1, -1*steering , velocity=speed)
    await runloop.until(turn_done)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    motor_pair.stop(motor_pair.PAIR_1)

async def spin_turn_cw(degrees,speed):
    global desired_degrees 
    desired_degrees = degrees
    # move with a steering of 50
    motor_pair.move_tank(motor_pair.PAIR_1, speed,-1*speed)
    await runloop.until(turn_done)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    motor_pair.stop(motor_pair.PAIR_1)

async def spin_turn_ccw(degrees,speed):
    global desired_degrees
    desired_degrees = degrees
    # move with a steering of 50
    motor_pair.move_tank(motor_pair.PAIR_1, -1*speed,speed)
    await runloop.until(turn_done)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    motor_pair.stop(motor_pair.PAIR_1)

async def  move_straight(distance):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance), 0)

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    await move_straight(40) # in cm 
    await spin_turn_ccw(70,200) # in degrees
    sys.exit("Finished")

runloop.run(main())