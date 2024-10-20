from hub import port, motion_sensor
import runloop, motor_pair, sys, motor, math, time

# cm, this is a constant for your robot
WHEEL_CIRCUMFERENCE = 17.5
# input must be in the same unit as WHEEL_CIRCUMFERENCE

wheel_diameter = 5.6 #cm

wheel_ports = [port.C, port.D]
lift_port = port.B

def degreesForDistance(distance_cm):
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360)

async def up_down():
    while not is_stopped():
        print('up')
        motor.run_for_degrees(lift_port, int(10/45.0 * 360), -100)
        await runloop.sleep_ms(500)
        await runloop.until(lambda: motor.velocity(lift_port) == 0)
        print('down')
        motor.run_for_degrees(lift_port, int(10/45.0 * 360), 100)
        await runloop.sleep_ms(500)
        await runloop.until(lambda: motor.velocity(lift_port) == 0)
    print('done with up/down')
    
def is_stopped():
    for p in [wheel_ports[0], wheel_ports[1], lift_port]:
        if motor.velocity(p) != 0:
            return False
    return True

async def main():
    motor_pair.pair(motor_pair.PAIR_1, *wheel_ports)
    motor_pair.move_for_degrees(motor_pair.PAIR_1, degreesForDistance(25),0,velocity=100)
    await up_down()
    sys.exit(0)

runloop.run(main())
