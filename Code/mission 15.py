from hub import port, motion_sensor
import runloop, motor_pair, sys, motor, math, time

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE
wheel_diameter = 5.6 #cm

VELOCITY = 500

def degreesForDistance(distance_cm):
    # Add multiplier for gear ratio if needed
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

async def move_straight_forward(distance):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -1*degreesForDistance(distance), 0, velocity=VELOCITY)
    #this is uncorrected, we need a corrective straight function as wheels are getting caught on the board

async def move__straight_backward(distance):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(distance), 0, velocity=VELOCITY)
    #this is uncorrected, we need a corrective straight function as wheels are getting caught on the board

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

async def dump():
    await motor.run_to_absolute_position(port.B,312,300)
    await motor.run_to_absolute_position(port.B,55,300)

async def move_straight_corrected(distance,speed):
    # convert arc to wheel rotation
    revolutions = distance / (math.pi*wheel_diameter)
    print("revs ", revolutions)
    # convert radians to degrees
    wheel_degrees = int (revolutions * 360)
    print("wheel degrees: ",wheel_degrees)
    motor_pair.unpair(motor_pair.PAIR_1) #need to unpair to reverse direction of bot
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.D) #reverse direction
    counter = 0

    error = 0
    correction = 0
    target_counter = distance * 400# Target based on distance characterization
    print("target counter is ",target_counter)
    counter = 0 # Start from 0
    starting_position = motor.reset_relative_position
    motion_sensor.reset_yaw(0)#set starting yaw angle
    while counter <= target_counter:
        error = motion_sensor.tilt_angles()[0]
        correction = error #can add some offset to correction, but leaving it as the same as the drifted angle works well
        motor_pair.move_tank(motor_pair.PAIR_1,int(speed+correction),int(speed-correction))
        counter += 1
    print("final counter value is ", counter)
    motor_pair.stop(motor_pair.PAIR_1)
    motor_pair.unpair(motor_pair.PAIR_1) #reset back to default for turns
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)

async def main():
    # Drive Base 1
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.E)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)
    
    #move out of the base and out on the table
    await move_straight(43,500)
    
    #turn to approach boat
    await spin_turn_cw(80,400)
    
    #go towards the boat
    await move_straight(23,300)
    
    #dump the stuff into the boat
    await dump()

    #back up from boat
    await move__straight_backward(6)
    
    #turn left to grab boat
    await spin_turn_ccw(85,300)
    
    #move forward to take boat forward
    await move_straight_corrected(13,400)

    #back up 
    await move__straight_backward(25)

    #turn around
    await spin_turn_ccw(85,400)

    #approach wall
    await move__straight_backward(10)

    #turn to face rear towards back of boat
    await spin_turn_ccw(90,300)


    sys.exit(0)

runloop.run(main())