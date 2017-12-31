import bpy
import math
import mathutils

from .get_fac import get_fac
from .get_pos_y import get_pos_y
from .get_pos_x import get_pos_x
from .rotate_point import rotate_point

def make_quad(seq):
    p = get_fac()
    w = bpy.context.scene.render.resolution_x * p/2
    h = bpy.context.scene.render.resolution_y * p/2
    
    vt = mathutils.Vector((get_pos_x(seq), get_pos_y(seq)))*p
    sc_x = w*seq.scale_start_x
    sc_y = sc_x if seq.use_uniform_scale else h*seq.scale_start_y
    rot = math.radians(seq.rotation_start)
    
    p0 = vt + rotate_point(mathutils.Vector((-sc_x, -sc_y)), rot)
    p1 = vt + rotate_point(mathutils.Vector((-sc_x, sc_y)), rot)
    p2 = vt + rotate_point(mathutils.Vector((sc_x, sc_y)), rot)
    p3 = vt + rotate_point(mathutils.Vector((sc_x, -sc_y)), rot)        
    
    sign_x = -1 if seq.use_flip_x else 1
    sign_y = -1 if seq.use_flip_y else 1
    
    p0 = mathutils.Vector((sign_x*p0.x,sign_y*p0.y))
    p1 = mathutils.Vector((sign_x*p1.x,sign_y*p1.y))
    p2 = mathutils.Vector((sign_x*p2.x,sign_y*p2.y))
    p3 = mathutils.Vector((sign_x*p3.x,sign_y*p3.y))
    
    return [p0, p1, p2, p3]
    
