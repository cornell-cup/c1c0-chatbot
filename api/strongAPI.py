from scheduler.config import * # Configurations

from typing import List # Typing

# data[elbow, spin, hand, shoulder]
# Elbow:    3-stop,  1-in,    2-out
# Spin:     3-stop,  1-CW,    2-CCW
# Hand:     3-stop,  1-close, 2-open
# Shoulder: 3-stop,  1-up,    2-down
data: List[int] = [3, 3, 3, 3]

def move_elbow(dir: int = 0) -> str:
    """
    Creates message with elbow updates based on the xbox controller input.

    @param dir: The direction of the elbow.
    @return: The message with elbow updates.
    """

    if dir == 1:   data[0] = 1
    elif dir == 2: data[0] = 2
    else:          data[0] = 3
    return strong_encode(data)

def move_spin(dir: int = 0) -> str:
    """
    Creates message with spin updates based on the xbox controller input.

    @param dir: The direction of the spin.
    @return: The message with spin updates.
    """

    if dir == 1:   data[1] = 1
    elif dir == 2: data[1] = 2
    else:          data[1] = 3
    return strong_encode(data)

def move_hand(dir: int = 0) -> str:
    """
    Creates message with hand updates based on the xbox controller input.

    @param dir: The direction of the hand.
    @return: The message with hand updates.
    """

    if dir == 1:   data[2] = 1
    elif dir == 2: data[2] = 2
    else:          data[2] = 3
    return strong_encode(data)

def move_shoulder(dir: int = 0):
    """
    Creates message with shoulder updates based on the xbox controller input.

    @param dir: The direction of the shoulder.
    @return: The message with shoulder updates.
    """

    if dir == 1:   data[3] = 1
    elif dir == 2: data[3] = 2
    else:          data[3] = 3
    return strong_encode(data)

def zero_strong() -> str:
    """
    Creates message with zero movement to send to scheduler.

    @return: The message with zero movement.
    """

    global data
    data = [3, 3, 3, 3]
    return strong_encode(data)

def strong_encode(data: List[int]) -> str:
    """
    Encodes the given movements into a message to send to the scheduler.

    @param data: The list of movements.
    @return: The message with the encoded movements.
    """

    return 'strong: ' + str(data)

def strong_decode(msg: str) -> List[int]:
    """
    Decodes the given message into a list of movements.

    @param msg: The message to decode.
    @return: The list of movements.
    """

    data       = str(msg)
    a, b, c, d = int(data[9]), int(data[12]), int(data[15]), int(data[18])
    return [a, b, c, d]
