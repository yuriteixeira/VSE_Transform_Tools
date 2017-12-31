import bpy
from .get_fac import get_fac

def view_zoom_preview():
    width = bpy.context.region.width
    height = bpy.context.region.height
    rv1 = bpy.context.region.view2d.region_to_view(0,0)
    rv2 = bpy.context.region.view2d.region_to_view(width-1,height-1)
    zoom = (1/(width/(rv2[0]-rv1[0])))/get_fac()
    return zoom
