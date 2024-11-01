def zero_rotate() -> str:
    """
    Call this method to return the head to 90 degrees.
    """

    return rotate_encode(0, 0, 1)

def left_rotate() -> str:
    """
    Call this method on left bumper to rotate head to the left at a predetermined rate.
    """

    return rotate_encode(5, 1, 0)

def right_rotate() -> str:
    """
    Call this method on right bumper to rotate head to the right at a predetermined rate.
    """

    return rotate_encode(5, 0, 0)

def turnToAngle(angle: int) -> str:
    """
    Call this method to turn to a specific angle between 0 and 202 degrees.
    """

    return rotate_encode(angle, 0, 1)

def rotate_encode(angle: int, negative: bool, absolute: bool) -> str:
    """
    Call this method to rotate the head to a specific angle or direction.

    @param angle: The angle to rotate the head to, 0 <= angle <= 202.
    @param negative: 1 if the angle is negative from the current position.
    @param absolute: 1 if the angle is an absolute angle, 0 if the angle is a change in angle.
    """

    return 'rotate: head rot: ' + str(angle) + str(absolute) + str(negative)

def rotate_decode(msg: str) -> str:
    """
    Decodes the given message into head rotation values.

    @param msg: The message to decode.
    @return: The head rotation values.
    """

    return msg[8:]
