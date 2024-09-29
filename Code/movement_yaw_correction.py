from hub import port, motion_sensor
import runloop, motor_pair, sys, motor, math, time

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE

wheel_diameter = 5.6 #cm

def degreesForDistance(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

async def move_straight_corrected(distance,speed):
    # convert arc to wheel rotation
    revolutions = distance / (math.pi*wheel_diameter)
    # convert radians to degrees
    wheel_degrees = int (revolutions * 360)
    motor_pair.unpair(motor_pair.PAIR_1)#need to unpair to reverse direction of bot
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.D) #reverse direction
    error = 0
    correction = 0
    target_counter = distance * 400# Target based on distance characterization
    counter = 0 # Start from 0
    starting_position = motor.reset_relative_position
    motion_sensor.reset_yaw(0)#set starting yaw angle
    while counter <= target_counter:
        error = motion_sensor.tilt_angles()[0]
        correction = error#can add some offset to correction, but leaving it as the same as the drifted angle works well
        motor_pair.move_tank(motor_pair.PAIR_1,int(speed+correction),int(speed-correction))
        #motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,wheel_degrees,-1*int(speed+correction),-1*int(speed-correction))
        #motor_pair.move_tank_for_time(motor_pair.PAIR_1,int(speed+correction),int(speed-correction),straight_time)
        counter += 1
    motor_pair.stop(motor_pair.PAIR_1)
    motor_pair.unpair(motor_pair.PAIR_1) #reset back to default for turns
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)

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
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    
    #await spin_turn_cw(180,100) # (degrees to turn, speed)
    #await spin_turn_ccw(180,100)
    await move_straight_corrected(15,500) # (distance, speed) distance is arbitrary, must figure out by experimenation
                                          # speed can be fast, but if you change speed it will affect distance, choose speed first
    await spin_turn_cw(45,200)
    await move_straight_corrected(16,300)

    sys.exit(0)

runloop.run(main())
