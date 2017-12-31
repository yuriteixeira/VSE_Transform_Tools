import bpy

def get_fac():
    if bpy.context.space_data.proxy_render_size == 'SCENE':
        fac = bpy.context.scene.render.resolution_percentage/100
    else:
        fac = 1    
    return fac
