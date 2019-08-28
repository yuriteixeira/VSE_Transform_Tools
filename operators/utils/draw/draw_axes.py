import bpy

from ..geometry.get_group_box import get_group_box
from ..geometry.get_preview_offset import get_preview_offset

from .draw_line import draw_line
from .draw_stippled_line import draw_stippled_line

from .colors import get_color_axis_x, get_color_axis_y


def draw_axes(self, context, angle):
    transforms = []
    strips = bpy.context.selected_sequences
    for strip in strips:
        if strip.type == 'TRANSFORM':
            transforms.append(strip)

    group_box = get_group_box(transforms)
    min_left, max_right, min_bottom, max_top = group_box
    group_width = max_right - min_left
    group_height = max_top - min_bottom

    group_pos_x = min_left + (group_width / 2)
    group_pos_y = min_bottom + (group_height / 2)

    offset_x, offset_y, fac, preview_zoom = get_preview_offset()

    x = (group_pos_x * fac * preview_zoom) + offset_x
    y = (group_pos_y * fac * preview_zoom) + offset_y

    color_axis_x = get_color_axis_x(context)
    color_axis_y = get_color_axis_y(context)
    thickness = 1
    stipple_length = 10
    far = 10000

    if self.choose_axis and not self.axis_y:
        draw_line([-far, y], [far, y], 2, color_axis_x)
        draw_stippled_line([x, -far], [x, far], thickness, stipple_length, color_axis_y)
    elif self.choose_axis and not self.axis_x:
        draw_stippled_line([-far, y], [far, y], thickness, stipple_length, color_axis_x)
        draw_line([x, -far], [x, far], thickness, color_axis_y)
    elif self.axis_x:
        draw_line([-far, y], [far, y], thickness, color_axis_x)
    elif self.axis_y:
        draw_line([x, -far], [x, far], thickness, color_axis_y)
