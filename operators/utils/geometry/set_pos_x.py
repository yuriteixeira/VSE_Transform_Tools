def set_pos_x(strip, pos):
    """
    Set the X position of either a transform strip or an unified transform-able strip

    :param strip: The strip
    :param pos:  the new X position in pixels (or percent for transform strip using it)
    """
    if strip.use_flip_x:
        pos = -pos

    if strip.type == "TRANSFORM":
        strip.translate_start_x = pos
    else:
        strip.transform.offset_x = pos
