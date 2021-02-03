def get_scale_x(strip):
    """
    Get X Scale for strip
    """
    if strip.type == "TRANSFORM":
        return strip.start_scale_x
    return strip.transform.scale_x
