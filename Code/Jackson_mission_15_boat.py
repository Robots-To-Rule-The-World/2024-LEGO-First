
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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance),0,velocity=speed)

async def dump():
    await motor.run_to_absolute_position(port.B,300,400)
    await motor.run_to_absolute_position(port.B,55,400)

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    runloop.sleep_ms(100)
    #going forward
    await move_straight(46,600)
    runloop.sleep_ms(100)
    #turn torwards boat
    await spin_turn_cw(90, 300)
    #aproach boat
    await move_straight(15,600)
    await dump()
    #move backwords
    await move_straight(12,-400)  #negative speed goes backwards
    runloop.sleep_ms(100)
    #turn torwards boat mast
    await spin_turn_ccw(7,300)
    #go forward
    await move_straight(6,600)
    
    runloop.sleep_ms(100)
    #turn left
    await spin_turn_ccw(50,150)
    #push boat
    await move_straight(29,300)
    runloop.sleep_ms(100)
    #turn left
    await spin_turn_ccw(8,300)
    #push boat more
    await move_straight(35,300)
    
    #go backword
    await move_straight(5,-300)
    
    runloop.sleep_ms(100)
    #straighten boat
    await spin_turn_cw(8,400)
    #wiggle boat
    await spin_turn_ccw(8,800)
    await spin_turn_cw(8,800)        
        
    sys.exit(0)

runloop.run(main())
