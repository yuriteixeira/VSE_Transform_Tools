import mathutils
import math

def rotate_point(p, angle):
    s = math.sin(angle);
    c = math.cos(angle);    
    v = mathutils.Vector((p.x * c - p.y * s, p.x * s + p.y * c))         
    return v
