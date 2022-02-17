def set_pos_y(strip, pos):
    """
    Set the Y position of either a transform strip or an unified transform-able strip

    :param strip: The strip
    :param pos:  the new Y position in pixels (or percent for transform strip using it)
    """
    if strip.use_flip_y:
        pos = -pos

    if strip.type == "TRANSFORM":
        strip.translate_start_y = pos
    else:
        strip.transform.offset_y = pos
