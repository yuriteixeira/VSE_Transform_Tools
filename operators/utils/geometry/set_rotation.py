import math


def set_rotation(strip, rot):
    """Set the rotation in degree for the given strip"""

    if strip.type == "TRANSFORM":
        strip.rotation_start = rot
    else:
        strip.transform.rotation = math.radians(rot)
