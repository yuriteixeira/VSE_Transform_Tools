"""
Utility functions to get colors from the user's theme. The functions convert colors to lists so we
can use them for drawing directly.
"""


def get_color_gizmo_primary(context):
    color = context.preferences.themes[0].user_interface.gizmo_primary
    return _color_to_list(color)


def get_color_gizmo_secondary(context):
    color = context.preferences.themes[0].user_interface.gizmo_secondary
    return _color_to_list(color)


def get_color_axis_x(context):
    color = context.preferences.themes[0].user_interface.axis_x
    return _color_to_list(color)


def get_color_axis_y(context):
    color = context.preferences.themes[0].user_interface.axis_y
    return _color_to_list(color)


def get_color_axis_z(context):
    color = context.preferences.themes[0].user_interface.axis_z
    return _color_to_list(color)


def _color_to_list(color):
    """Converts a Blender Color to a list of 4 color values to use with shaders and drawing"""
    return list(color) + [1.0]
