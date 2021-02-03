import math


def get_rotation(strip):
    """Get rotation angle in degree from strip"""
    if strip.type == "TRANSFORM":
        return strip.rotation_start

    return math.degrees(strip.transform.rotation)
