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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance),0,velocity=speed)

async def raise_arm(speed):
    await motor.run_to_absolute_position(port.B,300,speed)

async def lower_arm(speed):
    await motor.run_to_absolute_position(port.B,50,speed)

async def main():
    # Reset Base 1, do not change these lines
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
    motion_sensor.reset_yaw(0)
    
    await raise_arm(500)

    #go forward
    await move_straight(40,600)
    #turn right
    await spin_turn_cw(45,300)
    #move forward
    await move_straight(27,600)
    #turn torwards shark
    await spin_turn_ccw(100,300)
    #approach shark
    await move_straight(12,600)
    #yeet shark
    await lower_arm(2000)

    await runloop.sleep_ms(1000)

    #raise arm back up
    await raise_arm(600)


    #coral V
    await spin_turn_cw(80,300)
    await move_straight(11,600)
    await lower_arm(2000)
    await raise_arm(600)

    #raise mast
    await spin_turn_cw(90,300)
    await lower_arm(2000)
    await move_straight(10,600)
    await spin_turn_ccw(10,300)
    await raise_arm(2000)

    #return home V
    await spin_turn_cw(85,300)
    await move_straight(66,1100)


    sys.exit(0)

runloop.run(main())
