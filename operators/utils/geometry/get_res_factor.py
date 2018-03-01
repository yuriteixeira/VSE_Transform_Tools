import bpy


def get_res_factor():
    """
    Get the scene resolution percentage as a factor

    Returns
        :fac: The resolution factor (float)
    """
    fac = 1.0

    if bpy.context.space_data.proxy_render_size == 'SCENE':
        fac = bpy.context.scene.render.resolution_percentage / 100

    return fac
