import bpy
import math
import mathutils

from .draw_callback_draw_axes import draw_callback_draw_axes

def func_constraint_axis_mmb(self, context, key, value, angle): 
    if len(self.tab)>1:
        angle = 0
    if key == 'MIDDLEMOUSE' :
        if value == 'PRESS' :
            if self._handle_axes == None:
                args = (self, context, angle)
                self._handle_axes = bpy.types.SpaceSequenceEditor.draw_handler_add(
                    draw_callback_draw_axes, args, 'PREVIEW', 'POST_PIXEL')
            self.choose_axe = True
            self.pos_clic = self.pos_mouse
        if value == 'RELEASE' :
            self.choose_axe = False
            if self.pos_clic == self.pos_mouse:
                self.axe_x = self.axe_y = True
                if self._handle_axes:
                    bpy.types.SpaceSequenceEditor.draw_handler_remove(
                        self._handle_axes, 'PREVIEW')  
                    self._handle_axes = None
    if self.choose_axe :
        vec_axe_z = mathutils.Vector((0,0,1))
        vec_axe_x = mathutils.Vector((1,0,0))
        vec_axe_x.rotate(mathutils.Quaternion(vec_axe_z, math.radians(angle)))
        vec_axe_x = vec_axe_x.to_2d()
        vec_axe_y = mathutils.Vector((0,1,0))
        vec_axe_y.rotate(mathutils.Quaternion(vec_axe_z, math.radians(angle)))
        vec_axe_y = vec_axe_y.to_2d()
        
        ang_x = math.degrees(vec_axe_x.angle(self.vec_act))
        ang_y = math.degrees(vec_axe_y.angle(self.vec_act))
        
        if ang_x > 90:
            ang_x = 180 - ang_x
        if ang_y > 90:
            ang_y = 180 - ang_y   
            
        if ang_x < ang_y:
            self.axe_x = True
            self.axe_y = False
        else :
            self.axe_x = False
            self.axe_y = True
