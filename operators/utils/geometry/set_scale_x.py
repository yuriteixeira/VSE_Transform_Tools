def set_scale_x(strip, scale):
    """
    Set the X scale factor of either a transform strip or an unified transform-able strip

    :param strip: The strip
    :param scale:  the new X scale factor
    """
    if strip.type == "TRANSFORM":
        strip.scale_start_x = scale
    else:
        strip.transform.scale_x = scale
