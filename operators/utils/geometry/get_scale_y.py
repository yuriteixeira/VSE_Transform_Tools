def get_scale_y(strip):
    """
    Get Y Scale for strip
    """
    if strip.type == "TRANSFORM":
        return strip.start_scale_y
    return strip.transform.scale_y
