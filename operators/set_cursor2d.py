import bpy
import math
from mathutils import Vector

from .utils import get_visible_strips
from .utils import rotate_point
from .utils import get_transform_box
from .utils import get_strip_box
from .utils import get_strip_corners

class SetCursor2d(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/1uTD9C1.gif)
    Set the pivot point (point of origin) location. This will affect 
    how strips are rotated and scaled.
    """
    bl_label = "Set Cursor2D"
    bl_idname = "vse_transform_tools.set_cursor2d"
    bl_description = "Set the pivot point location"

    @classmethod
    def poll(cls, context):
        if (context.scene.sequence_editor and
                context.scene.seq_pivot_type == '2'):
            return True
        return False

    def invoke(self, context, event):
        bpy.ops.vse_transform_tools.initialize_pivot()

        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y

        pos = context.region.view2d.region_to_view(mouse_x, mouse_y)
        mouse_pos = Vector(pos)
        
        if event.ctrl:
            snap_points = get_important_edge_points()
            point = min(snap_points, key = lambda x: (x - mouse_pos).length)
            point.x = round(point.x)
            point.y = round(point.y)
            
            context.scene.seq_cursor2d_loc = [int(point.x), int(point.y)]
        
        else:
            context.scene.seq_cursor2d_loc = [round(pos[0]), round(pos[1])]

        return {'PASS_THROUGH'}


def get_important_edge_points():
    """
    Get the edge locations for where a user may want to snap the cursor
    to.
    """
    scene = bpy.context.scene
    
    strips = get_visible_strips()
    
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    
    bl = Vector([0, 0])
    l = Vector([0, res_y / 2])
    tl = Vector([0, res_y])
    t = Vector([res_x / 2, res_y])
    tr = Vector([res_x, res_y])
    r = Vector([res_x, res_y / 2])
    br = Vector([res_x, 0])
    b = Vector([res_x / 2, 0])
    origin = Vector([res_x / 2, res_y / 2])
    
    vectors = [bl, l, tl, t, tr, r, br, b, origin]
    
    for vec in vectors:
        vec.x -= (res_x / 2)
        vec.y -= (res_y / 2)
    
    
    important_edge_points = vectors
    for strip in strips:
        if strip.type == "TRANSFORM":
            left, right, bottom, top = get_transform_box(strip)
        
        else:
            left, right, bottom, top = get_strip_box(strip)
    
        mid_x = left+ ((right - left) / 2)
        mid_y = bottom + ((top - bottom) / 2)
        l = Vector([left, mid_y])
        r = Vector([right, mid_y])
        t = Vector([mid_x, top])
        b = Vector([mid_x, bottom])
        
        origin = Vector([mid_x, mid_y])
        
        if strip.type == "TRANSFORM":
            angle = math.radians(strip.rotation_start)
            l = rotate_point(l, angle, origin=origin)
            r = rotate_point(r, angle, origin=origin)
            t = rotate_point(t, angle, origin=origin)
            b = rotate_point(b, angle, origin=origin) 

        bl, tl, tr, br = get_strip_corners(strip)
        
        vectors = [bl, l, tl, t, tr, r, br, b, origin]
        
        for vec in vectors:
            vec.x -= (res_x / 2)
            vec.y -= (res_y / 2)
        
        important_edge_points.extend(vectors)
    
    return important_edge_points
