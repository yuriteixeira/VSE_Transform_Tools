def get_scale_y(strip):
    """
    Get Y Scale for strip
    """
    if strip.type == "TRANSFORM":
        return getattr(strip, "start_scale_y", getattr(strip, "scale_start_y"))
    return strip.transform.scale_y
