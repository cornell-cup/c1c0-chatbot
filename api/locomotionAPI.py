from scheduler.config import * # Configurations

def zero_locomotion() -> str:
    """
    Creates message with zero movement to send to scheduler.

    @return: The message with zero movement.
    """

    lvalue = '+' + str(0.) + '0'
    rvalue = '+' + str(0.) + '0'
    return locomotion_encode(lvalue, rvalue)

def get_locomotion(axis_x, axis_y) -> str:
    """
    Creates message with movement updates based on the joystick input.

    @param axis_x: The x-axis direction of the joystick.
    @param axis_y: The y-axis direction of the joystick.
    @return: The message with movement updates.
    """
    lvalue, rvalue, motor_val = 0, 0, .9

    if (axis_x == 1 and axis_y == 1):
        lvalue = '+' + str(motor_val) + '0'
        rvalue = '+' + str(round(.6,1)) + '0'
    elif (axis_x == -1 and axis_y == -1):
        lvalue = '+' + str(0.) + '0'
        rvalue = '+' + str(motor_val) + '0'
    elif (axis_x == 0 and axis_y == 1):
        lvalue = '+' + str(motor_val) + '0'
        rvalue = '+' + str(motor_val) + '0'
    elif (axis_x == 0 and axis_y == -1):
        lvalue = '-' + str(motor_val) + '0'
        rvalue = '-' + str(motor_val) + '0'
    elif (axis_x == -1 and axis_y == 0):
        lvalue = '-' + str(motor_val) + '0'
        rvalue = '+' + str(motor_val) + '0'
    elif (axis_x == 1 and axis_y == 0):
        lvalue = '+' + str(motor_val) + '0'
        rvalue = '-' + str(motor_val) + '0'
    elif (axis_x == 1 and axis_y == 0):
        lvalue = '+' + str(motor_val) + '0'
        rvalue = '-' + str(motor_val) + '0'
    else:
        lvalue = '+' + str(0.) + '0'
        rvalue = '+' + str(0.) + '0'


    return locomotion_encode(lvalue, rvalue)

def locomotion_encode(lvalue: str, rvalue: str) -> str:
    """
    Encodes the given movements into a message to send to the scheduler.

    @param lvalue: The left movement value.
    @param rvalue: The right movement value.
    @return: The message with the encoded movements.
    """

    return 'locomotion: (' + str(lvalue) + ',' + str(rvalue) + ')'

def locomotion_decode(message: str) -> str:
    """
    Decodes the given message into a movement string.

    @param message: The message to decode.
    @return: The movement string decoded from the message.
    """

    return message.split(': ')[1]
