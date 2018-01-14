import bpy
import math
from mathutils import Vector

from .tf_utils import process_input
from .tf_utils import get_res_factor
from .tf_utils import rotate_point
from .tf_utils import get_pos_x
from .tf_utils import get_pos_y
from .tf_utils import set_pos_x
from .tf_utils import set_pos_y

from .tf_utils import draw_callback_px_point

class TF_Rotate(bpy.types.Operator):
    bl_idname = "sequencer.tf_rotate"
    bl_label = "Transform Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    first_mouse = Vector([0, 0])
    tab_init = []
    tab_init_t = []
    tab = []

    center_area = Vector([0, 0])
    center_real = Vector([0, 0])
    
    vec_init = Vector([0, 0])
    vec_act = Vector([0, 0])

    key_val = ''
    key_period = False
    key_period_val = 1
    
    rot_marker = 0
    revolutions = 0
    
    slow_factor = 10
    pre_slow_rot = 0
    post_slow_rot = 0

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
        scene.sequence_editor.active_strip and
        scene.sequence_editor.active_strip and
        scene.sequence_editor.active_strip.type == 'TRANSFORM' and 
        context.space_data.type == 'SEQUENCE_EDITOR' and
        context.region.type == 'PREVIEW'):
            return True
        return False
        
    def modal(self, context, event):
        context.area.tag_redraw()

        if self.tab:
            self.vec_act = Vector(
                (event.mouse_region_x, event.mouse_region_y)) 
            self.vec_act -= self.center_area
            
            rot =  math.degrees(
                -self.vec_init.angle_signed(self.vec_act)) 
            rot += self.post_slow_rot

            if rot < 0 and self.rot_marker > 0:
                rot = 360 + rot
            elif rot > 0 and self.rot_marker < 0:
                rot = rot - 360
            
            if self.rot_marker < rot and self.rot_marker - rot <= -180:
                self.revolutions -= 1
            elif self.rot_marker > rot and self.rot_marker - rot >= 180:
                self.revolutions += 1
            
            self.rot_marker = rot
            
            if 'SHIFT' in event.type and event.value == 'PRESS':
                self.pre_slow_rot = rot + (self.revolutions * 360)
            
            elif 'SHIFT' in event.type and event.value == 'RELEASE':
                rev_degs = self.revolutions * 360
                slow_fac = (self.slow_factor - 1) / self.slow_factor
                
                self.post_slow_rot += self.pre_slow_rot - rot - rev_degs
                self.post_slow_rot *= slow_fac
                
                rot = rev_degs + (rot - self.pre_slow_rot)
                rot /= self.slow_factor
                rot += self.pre_slow_rot
                
                self.pre_slow_rot = 0

            elif event.shift:
                rev_degs = self.revolutions * 360
                
                rot = rev_degs + (rot - self.pre_slow_rot)
                rot /= self.slow_factor
                rot += self.pre_slow_rot
            
            rot = rot % 360
            if rot < -180:
                rot = rot + 360
            elif rot > 180:
                rot = rot - 360
            
            process_input(self, event.type, event.value)
            if self.key_val != '':
                try:
                    rot = float(self.key_val)
                except ValueError:
                    pass
            
            for i in range(len(self.tab)):
                strip = self.tab[i]
                init_rot = self.tab_init[i]
                init_t = self.tab_init_t[i]
                
                if init_rot <-180:
                    init_rot = 360 + init_rot
                if init_rot > 180:
                    init_rot = -360 + init_rot
                
                flip_x = 1
                if strip.use_flip_x:
                    flip_x = -1
                
                flip_y = 1
                if strip.use_flip_y:
                    flip_y = -1

                strip_rot = init_rot + flip_x * flip_y * rot
                
                rotation_increment = 5
                if event.ctrl:
                    strip_rot = int(strip_rot / rotation_increment) 
                    strip_rot *= rotation_increment
                
                pivot_type = context.scene.seq_pivot_type
                
                if (pivot_type == '1' or 
                   pivot_type in ['0', '3'] and len(self.tab) == 1):
                    strip.rotation_start = strip_rot

                elif pivot_type in ['0','3'] and len(self.tab) > 1:
                    pos_init = Vector([init_t[0], init_t[1]])
                    
                    pos_flip_x = flip_x * self.center_real.x 
                    pos_flip_y = flip_y * self.center_real.y
                    pos_flip = Vector([pos_flip_x, pos_flip_y])
                    
                    pos_init -= pos_flip
                    point_rot = flip_x * flip_y * math.radians(rot)
                    
                    np = rotate_point(pos_init, point_rot)
                    if event.ctrl:
                        p_rot_degs = math.radians(strip_rot - init_rot)
                        point_rot = flip_x * flip_y * p_rot_degs
                        np = rotate_point(pos_init, point_rot)
                    
                    pos_x = np.x + flip_x * self.center_real.x
                    pos_x = set_pos_x(strip, pos_x)
                    
                    pos_y = np.y + flip_y * self.center_real.y
                    pos_y = set_pos_y(strip, pos_y)
                    
                    if np.x == 0 and np.y == 0:
                        strip.rotation_start = strip_rot
                        
                    else:
                        strip.rotation_start = strip_rot
                        strip.translate_start_x = pos_x
                        strip.translate_start_y = pos_y

                elif pivot_type == '2':
                    fac = get_res_factor()
                    
                    pos_x = flip_x * context.scene.seq_cursor2d_loc[0]
                    pos_y = flip_y * context.scene.seq_cursor2d_loc[1]
                    
                    center_c2d = Vector([pos_x, pos_y])
                    center_c2d /= fac
                    
                    pos_init = Vector([init_t[0], init_t[1]])
                    pos_init -= center_c2d
                    
                    point_rot = flip_x * flip_y * math.radians(rot)
                    
                    np = rotate_point(pos_init, point_rot)
                    if event.ctrl:
                        p_rot_degs = math.radians(strip_rot - init_rot)
                        point_rot = flip_x * flip_y * p_rot_degs
                        np = rotate_point(pos_init, point_rot)
                    
                    strip.rotation_start = strip_rot
                    
                    pos_x = set_pos_x(strip, np.x + center_c2d.x)
                    pos_y = set_pos_y(strip, np.y + center_c2d.y)
                    
                    strip.translate_start_x = pos_x
                    strip.translate_start_y = pos_y

            info_rot = (rot)
            context.area.header_text_set("Rotation %.4f " % info_rot)

        if (event.type == 'LEFTMOUSE' or 
           event.type == 'RET' or 
           event.type == 'NUMPAD_ENTER' or 
           not self.tab):
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self._handle_line, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        if event.type == 'ESC' or event.type == 'RIGHTMOUSE':
            for i in range(len(self.tab)):
                strip = self.tab[i]
                init_rot = self.tab_init[i]
                init_t = self.tab_init_t[i]
                
                strip.rotation_start = init_rot
                strip.translate_start_x = set_pos_x(strip, init_t[0])
                strip.translate_start_y = set_pos_y(strip, init_t[1])
            
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self._handle_line, 'PREVIEW')
            context.area.header_text_set()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        scene = context.scene
        view2d = context.region.view2d
        
        bpy.ops.sequencer.tf_initialize_pivot()
        
        if event.alt:
            for strip in context.selected_sequences:
                if strip.type == 'TRANSFORM':
                    strip.rotation_start = 0.0
            return {'FINISHED'}
        
        else:
            fac = get_res_factor()
            self.tab_init = []
            self.tab = []
            self.tab_init_t = []
            self.center_real = Vector([0, 0])
            self.center_area = Vector([0, 0])
            self.key_val = ''
            rotated_count = 0

            for strip in context.selected_sequences:
                if strip.type == 'TRANSFORM':
                    pos_x = get_pos_x(strip)
                    pos_y = get_pos_y(strip)
                    
                    self.tab_init.append(strip.rotation_start)
                    self.tab_init_t.append([pos_x, pos_y])
                    self.tab.append(strip)
                    
                    flip_x = 1
                    if strip.use_flip_x:
                        flip_x = -1
                    
                    flip_y = 1
                    if strip.use_flip_y:
                        flip_y = -1
                    
                    self.center_real += Vector((
                        flip_x * pos_x, flip_y * pos_y))
                    self.center_area += Vector((
                        flip_x * pos_x, flip_y * pos_y))
                    
                    rotated_count += 1

            if self.tab:
                self.center_real /= rotated_count
                if context.scene.seq_pivot_type == '2':
                    cur_loc = context.scene.seq_cursor2d_loc
                    pos = view2d.view_to_region(cur_loc[0], cur_loc[1])
                    self.center_area = Vector(pos)
                    
                elif context.scene.seq_pivot_type == '3':
                    active_strip = scene.sequence_editor.active_strip
                    
                    flip_x = 1
                    if strip.use_flip_x:
                        flip_x = -1
                    
                    flip_y = 1
                    if strip.use_flip_y:
                        flip_y = -1
                    
                    pos_x = get_pos_x(active_strip)
                    pos_y = get_pos_y(active_strip)
                    
                    self.center_real = Vector((
                        flip_x * pos_x, flip_y * pos_y))
                    
                    pos_x *= flip_x * fac
                    pos_y *= flip_y * fac
                    
                    view_2d = context.region.view2d
                    pos = view_2d.view_to_region(pos_x, pos_y)
                    self.center_area = Vector(pos)
                    
                else:
                    self.center_area /= rotated_count
                    
                    pos_x = self.center_area.x * fac
                    pos_y = self.center_area.y * fac
                    pos = view2d.view_to_region(
                        pos_x, pos_y, clip=False)
                    self.center_area = Vector(pos)
                    
                self.vec_init = Vector(
                    (event.mouse_region_x, event.mouse_region_y)) 
                self.vec_init -= self.center_area
                
            args = (self, context)
            self._handle_line = bpy.types.SpaceSequenceEditor.draw_handler_add(
                draw_callback_px_point, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'

        return {'RUNNING_MODAL'}
