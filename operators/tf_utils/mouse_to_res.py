import bpy
from mathutils import Vector

from .get_res_factor import get_res_factor

def mouse_to_res(mouse_vec):
    '''Convert mouse click position to pixel position'''
    scene = bpy.context.scene
    
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    
    mouse_x = mouse_vec.x
    mouse_y = mouse_vec.y
    
    fac = get_res_factor()
            
    pos = bpy.context.region.view2d.region_to_view(mouse_x, mouse_y)
    
    pos_x = (pos[0] + (res_x * fac / 2)) / fac
    pos_y = (pos[1] + (res_y * fac / 2)) / fac
    
    mouse_res = Vector((pos_x, pos_y))
    return mouse_res
