import bpy


def prepare_set_pos_y(strip, pos):
    """
    Set the Y position of a transform strip, accounting for whether or
    not the translation unit is set to PERCENT

    Args
        :strip: The transform strip (bpy.types.Sequence)
        :pos:   The X position the strip should be moved to, in pixels
                (int)
    """
    res_y = bpy.context.scene.render.resolution_y

    if strip.type == "TRANSFORM" and strip.translation_unit == 'PERCENT':
        pos = pos * 100 / res_y

    return pos


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
