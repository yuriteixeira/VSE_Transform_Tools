import bpy

def get_res_factor():
    '''Get the resolution percentage as a factor'''
    fac = 1
    if bpy.context.space_data.proxy_render_size == 'SCENE':
        fac = bpy.context.scene.render.resolution_percentage / 100
    return fac
