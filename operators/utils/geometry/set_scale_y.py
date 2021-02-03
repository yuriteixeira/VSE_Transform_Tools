def set_scale_y(strip, scale):
    """
    Set the Y scale factor of either a transform strip or an unified transform-able strip

    :param strip: The strip
    :param scale:  the new Y scale factor
    """
    if strip.type == "TRANSFORM":
        strip.scale_start_y = scale
    else:
        strip.transform.scale_y = scale
