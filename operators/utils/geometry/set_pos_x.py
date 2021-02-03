import bpy


def prepare_set_pos_x(strip, pos):
    """
    Set the X position of a transform strip, accounting for whether or
    not the translation unit is set to PERCENT

    Args
        :strip: The transform strip (bpy.types.Sequence)
        :pos:   The X position the strip should be moved to, in pixels
                (int)
    """
    res_x = bpy.context.scene.render.resolution_x

    if strip.type == "TRANSFORM" and strip.translation_unit == 'PERCENT':
        pos = (pos * 100) / res_x

    return pos


def set_pos_x(strip, pos):
    """
    Set the X position of either a transform strip or an unified transform-able strip

    :param strip: The strip
    :param pos:  the new X position in pixels (or percent for transform strip using it)
    """
    if strip.type == "TRANSFORM":
        strip.translate_start_x = pos
    else:
        strip.transform.offset_x = pos
