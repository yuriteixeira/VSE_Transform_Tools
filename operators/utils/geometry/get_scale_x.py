def get_scale_x(strip):
    """
    Get X Scale for strip
    """
    if strip.type == "TRANSFORM":
        return getattr(strip, "start_scale_x", getattr(strip, "scale_start_x"))
    return strip.transform.scale_x
