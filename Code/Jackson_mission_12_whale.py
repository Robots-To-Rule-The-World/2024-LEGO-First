454748495051525354606162634443424140465556575859
    await runloop.until(motion_sensor.stable)    await move_straight(72,400)    await spin_turn_cw(35,300)    await move_straight(13,500)    await dump()    #return to base    await move_straight(35, -600)    await spin_turn_cw(100,300)    motion_sensor.reset_yaw(0)    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)    # Drive Base 1async def main():    await move_straight(30,800)    await spin_turn_cw(105,300)    await move_straight(138,1100)    await spin_turn_ccw(20,300)    await move_straight(7,600)

    #return to base
    await move_straight(35, -600)
    await spin_turn_cw(100,300)
    await move_straight(30,800)
    await spin_turn_cw(105,300)
    await move_straight(138,1100)
    await spin_turn_ccw(20,300)
    await move_straight(7,600)


SystemExit: 01:02:46 PM: Compiled-------------Traceback (most recent call last):  File "Whale 1", line 66, in <module>  File "Whale 1", line 64, in mainSystemExit: 0
Getting Started
API Modules
