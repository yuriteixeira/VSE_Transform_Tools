import bpy
import bgl
import copy

import math
from mathutils import Vector
from mathutils.geometry import intersect_point_quad_2d
from mathutils.geometry import intersect_line_line_2d

from .tf_utils import get_transform_box
from .tf_utils import get_strip_corners
from .tf_utils import get_preview_offset
from .tf_utils import rotate_point

from .tf_utils import get_pos_x
from .tf_utils import get_pos_y
from .tf_utils import set_pos_x
from .tf_utils import set_pos_y

def get_perpendicular_point(pt, bl, tl, tr, br):
    '''
    Return the point if it is inside the quad, else, return
    a point on the border of the quad
    '''
    
    intersects = intersect_point_quad_2d(
        pt, bl, tl, tr, br)
    
    if intersects:
        return pt
    
    elif pt.x <= bl.x and pt.y <= bl.y:
        return Vector(bl)
    elif pt.x <= tl.x and pt.y >= tl.y:
        return Vector(tl)
    elif pt.x >= tr.x and pt.y >= tr.y:
        return Vector(tr)
    elif pt.x >= br.x and pt.y <= br.y:
        return Vector(br)
    
    max_x = max([tr.x, br.x])
    min_x = min([tl.x, bl.x])
    
    max_y = max([tl.y, tr.y])
    min_y = min([bl.y, br.y])
    
    # pt left of left side
    if (pt.x <= tl.x or pt.x <= bl.x) and (pt.y >= bl.y and pt.y <= tl.y):
        right = Vector([max_x, pt.y])
        intersection = intersect_line_line_2d(bl, tl, pt, right)
    
    # pt right of right side
    elif (pt.x >= br.x or pt.x >= tr.x) and (pt.y >= br.y and pt.y <= tr.y):
        left = Vector([min_x, pt.y])
        intersection = intersect_line_line_2d(br, tr, pt, left)
    
    # pt above top side
    elif (pt.y >= tl.y or pt.y >= tr.y) and (pt.x >= tl.x and pt.x <= tr.x):
        bottom = Vector([pt.x, min_y])
        intersection = intersect_line_line_2d(tl, tr, pt, bottom)
    
    # pt below bottom side
    elif (pt.y <= bl.y or pt.y <= br.y) and (pt.x >= bl.x and pt.x <= br.x):
        top = Vector([pt.x, max_y])
        intersection = intersect_line_line_2d(bl, br, pt, top)
        
    return intersection

def draw_callback_px_crop(self, context):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glColor4f(0.0, 1.0, 1.0, 1.0)
    
    active_strip = context.scene.sequence_editor.active_strip
    angle = math.radians(active_strip.rotation_start)
    
    theme = context.user_preferences.themes['Default']
    active_color = theme.view_3d.object_active
    
    self.set_corners(context)
    self.set_quads(context)
    
    # Edges
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for corner in self.corners:
        bgl.glVertex2f(corner[0], corner[1])
    bgl.glEnd()
    
    sin = math.sin(angle)
    cos = math.cos(angle)
    
    # Points
    for i in range(len(self.corner_quads)):
        quad = self.corner_quads[i]
        
        bl = quad[0]
        tl = quad[1]
        tr = quad[2]
        br = quad[3]
        
        if self.clicked_quad == i:
            bgl.glColor4f(
                active_color[0], active_color[1], active_color[2], 1.0)
        else:
            bgl.glColor4f(0.0, 1.0, 1.0, 1.0)
        
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glVertex2f(bl[0], bl[1])
        bgl.glVertex2f(tl[0], tl[1])
        bgl.glVertex2f(tr[0], tr[1])
        bgl.glVertex2f(br[0], br[1])
        bgl.glEnd()

class TF_Crop(bpy.types.Operator):
    bl_idname = "sequencer.tf_crop"
    bl_label = "Draw the crop"
    bl_options = {'REGISTER', 'UNDO'}
    
    init_pos_x = 0
    init_pos_y = 0
    
    mouse_pos = Vector([-1, -1])
    current_mouse = Vector([-1, -1])
    
    corners = [Vector([-1, -1]), Vector([-1, -1]), Vector([-1, -1]), 
               Vector([-1, -1])]
    max_corners = [Vector([-1, -1]), Vector([-1, -1]), Vector([-1, -1]), 
                   Vector([-1, -1])]
    corner_quads = []
    
    clicked_quad = None
    
    handle_crop = None
    
    crop_left = 0
    crop_right = 0
    crop_bottom = 0
    crop_top = 0
    
    scale_factor_x = 1.0
    scale_factor_y = 1.0
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
           scene.sequence_editor.active_strip and
           scene.sequence_editor.active_strip.type == 'TRANSFORM' and
           scene.sequence_editor.active_strip.select and
           context.space_data.type == 'SEQUENCE_EDITOR' and
           context.region.type == 'PREVIEW'):
            return True
        return False
    
    def crop_scale(self, strip, crops):
        '''
        Set the strip_in crop and the strip's scale
        '''
        context = bpy.context
        scene = context.scene
        
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y
        
        left, right, bottom, top = get_transform_box(strip)
        width = right - left
        height = top - bottom
        
        strip_in = strip.input_1
        
        crop_left, crop_right, crop_bottom, crop_top = crops
        
        rot = math.radians(strip.rotation_start)
        
        cos = math.cos(rot)
        sin = math.sin(rot)
        
        crop_xl = strip_in.crop.min_x
        crop_xr = strip_in.crop.max_x
        crop_yb = strip_in.crop.min_y
        crop_yt = strip_in.crop.max_y

        crop_adjust_l = crop_left - crop_xl
        crop_adjust_r = crop_right - crop_xr
        crop_adjust_b = crop_bottom - crop_yb
        crop_adjust_t = crop_top - crop_yt
        
        proxy_facs = {
            'NONE' : 1.0,
            'SCENE' : 1.0,
            'FULL' : 1.0,
            'PROXY_100' : 1.0,
            'PROXY_75' : 0.75,
            'PROXY_50' : 0.5,
            'PROXY_25' : 0.25
        }
        
        proxy_key = context.space_data.proxy_render_size
        proxy_fac = proxy_facs[proxy_key]
        
        orig_width = res_x
        orig_height = res_y
        if hasattr(strip_in, 'elements'):
            orig_width = strip_in.elements[0].orig_width
            orig_height = strip_in.elements[0].orig_height
            
            orig_width /= proxy_fac
            orig_height /= proxy_fac
        
        strip_in.crop.min_x = crop_left
        strip_in.crop.max_x = crop_right
        strip_in.crop.min_y = crop_bottom
        strip_in.crop.max_y = crop_top
        
        # Find the scale_x growth factor
        scl_x = 0
        if orig_width - crop_left - crop_right > 0:
            scl_x = (orig_width - crop_left - crop_right) / (orig_width - crop_xl - crop_xr)
        
        scl_y = 0
        if orig_height - crop_top - crop_bottom > 0:
            scl_y = (orig_height - crop_bottom - crop_top) / (orig_height - crop_yb - crop_yt)
        
        strip.scale_start_x *= scl_x
        strip.scale_start_y *= scl_y
        
        # Find the translation difference between old and new
        width_diff = (width * scl_x) - width
        height_diff = (height * scl_y) - height
        
        left_shift = 0
        right_shift = 0
        if abs(crop_adjust_l + crop_adjust_r) > 0:
            left_shift = width_diff * (crop_adjust_l / (crop_adjust_l + crop_adjust_r))
            right_shift = width_diff * (crop_adjust_r / (crop_adjust_l + crop_adjust_r))
        
        bottom_shift = 0
        top_shift = 0
        if abs(crop_adjust_b + crop_adjust_t) > 0:
            bottom_shift = height_diff * (crop_adjust_b / (crop_adjust_b + crop_adjust_t))
            top_shift = height_diff * (crop_adjust_t / (crop_adjust_b + crop_adjust_t))
        
        pos_x = get_pos_x(strip)
        pos_y = get_pos_y(strip)
        
        pos_x -= (left_shift * cos) / 2
        pos_x += (right_shift * cos) / 2
        pos_x += (bottom_shift * sin) / 2
        pos_x -= (top_shift * sin) / 2
        
        pos_y -= (bottom_shift * cos) / 2
        pos_y += (top_shift * cos) / 2
        pos_y -= (left_shift * sin) / 2
        pos_y += (right_shift * sin) / 2
        
        strip.translate_start_x = set_pos_x(strip, pos_x)
        strip.translate_start_y = set_pos_y(strip, pos_y)
        
        self.scale_factor_x = (res_x / orig_width) * strip.scale_start_x
        self.scale_factor_y = (res_y / orig_height) * strip.scale_start_y
        
        self.init_crop_left = crop_xl
        self.init_crop_right = crop_xr 
        self.init_crop_bottom = crop_yb
        self.init_crop_top = crop_yt
        
        offset_x, offset_y, fac, preview_zoom = get_preview_offset()
        self.crop_left = crop_xl * self.scale_factor_x
        self.crop_right = crop_xr * self.scale_factor_x
        self.crop_bottom = crop_yb * self.scale_factor_y
        self.crop_top = crop_yt * self.scale_factor_y
        
    def set_corners(self, context):
        active_strip = context.scene.sequence_editor.active_strip
        angle = math.radians(active_strip.rotation_start)
        
        sin = math.sin(angle)
        cos = math.cos(angle)
        
        offset_x, offset_y, fac, preview_zoom = get_preview_offset()
        
        self.max_corners = get_strip_corners(active_strip)
        for corner in self.max_corners:
            corner.x = (corner.x * preview_zoom * fac) + offset_x
            corner.y = (corner.y * preview_zoom * fac) + offset_y
        
        origin = self.max_corners[2] - self.max_corners[0]

        bl = rotate_point(self.max_corners[0], -angle, origin)
        tl = rotate_point(self.max_corners[1], -angle, origin)
        tr = rotate_point(self.max_corners[2], -angle, origin)
        br = rotate_point(self.max_corners[3], -angle, origin)
        
        vec = self.current_mouse - self.mouse_pos
        
        crop_left = self.crop_left * preview_zoom * fac
        crop_bottom = self.crop_bottom * preview_zoom * fac
        crop_top = self.crop_top * preview_zoom * fac
        crop_right = self.crop_right * preview_zoom * fac
        
        cushion = 10
        if self.clicked_quad != None:
            for i in range(len(self.max_corners)):
                if self.clicked_quad == 0: # Bottom Left Clicked
                    pt_x = bl.x + (vec.x * cos) + (vec.y * sin) + crop_left
                    pt_y = bl.y + (vec.y * cos) - (vec.x * sin) + crop_bottom
                    pt = get_perpendicular_point(
                        Vector([pt_x, pt_y]), bl, tl, tr, br)
                    
                    self.corners[2].x = tr.x - crop_right
                    self.corners[2].y = tr.y - crop_top

                    if pt.x > self.corners[2].x - cushion:
                        pt.x = self.corners[2].x - cushion
                    if pt.y > self.corners[2].y - cushion:
                        pt.y = self.corners[2].y - cushion

                    self.corners[0] = pt

                    self.corners[1].x = tl.x + (pt.x - bl.x)
                    self.corners[1].y = tl.y - crop_top
                    
                    self.corners[3].x = br.x - crop_right
                    self.corners[3].y = br.y + (pt.y - bl.y)

                    break
                
                elif self.clicked_quad == 1: # Top Left Clicked
                    pt_x = tl.x + (vec.x * cos) + (vec.y * sin) + crop_left
                    pt_y = tl.y + (vec.y * cos) - (vec.x * sin) - crop_top
                    pt = get_perpendicular_point(
                        Vector([pt_x, pt_y]), bl, tl, tr, br)
                    
                    self.corners[3].x = br.x - crop_right
                    self.corners[3].y = br.y + crop_bottom
                    
                    if pt.x > self.corners[3].x - cushion:
                        pt.x = self.corners[3].x - cushion
                    if pt.y < self.corners[3].y + cushion:
                        pt.y = self.corners[3].y + cushion
                    
                    self.corners[1] = pt
                    
                    self.corners[0].x = bl.x + (pt.x - tl.x)
                    self.corners[0].y = bl.y + crop_bottom
                    
                    self.corners[2].x = tr.x - crop_right
                    self.corners[2].y = tr.y - (tl.y - pt.y)
                    
                    break
                
                elif self.clicked_quad == 2: # Top Right Clicked
                    pt_x = tr.x + (vec.x * cos) + (vec.y * sin) - crop_right
                    pt_y = tr.y + (vec.y * cos) - (vec.x * sin) - crop_top
                    pt = get_perpendicular_point(
                        Vector([pt_x, pt_y]), bl, tl, tr, br)
                    
                    self.corners[0].x = bl.x + crop_left
                    self.corners[0].y = bl.y + crop_bottom
                    
                    if pt.x < self.corners[0].x + cushion:
                        pt.x = self.corners[0].x + cushion
                    if pt.y < self.corners[0].y + cushion:
                        pt.y = self.corners[0].y + cushion
                    
                    self.corners[2] = pt
                    
                    self.corners[1].x = tl.x + crop_left
                    self.corners[1].y = tl.y - (tr.y - pt.y)
                    
                    self.corners[3].x = br.x - (tr.x - pt.x)
                    self.corners[3].y = br.y + crop_bottom
                
                elif self.clicked_quad == 3: # Bottom Right Clicked
                    pt_x = br.x + (vec.x * cos) + (vec.y * sin) - crop_right
                    pt_y = br.y + (vec.y * cos) - (vec.x * sin) + crop_bottom
                    pt = get_perpendicular_point(
                        Vector([pt_x, pt_y]), bl, tl, tr, br)
    
                    self.corners[1].x = tl.x + crop_left
                    self.corners[1].y = tl.y - crop_top

                    if pt.x < self.corners[1].x + cushion:
                        pt.x = self.corners[1].x + cushion
                    if pt.y > self.corners[1].y - cushion:
                        pt.y = self.corners[1].y - cushion
                    
                    self.corners[3] = pt
                    
                    self.corners[0].x = bl.x + crop_left
                    self.corners[0].y = bl.y + (pt.y - br.y)
                    
                    self.corners[2].x = tr.x - (tr.x - pt.x)
                    self.corners[2].y = tr.y - crop_top
                    
        else:
            self.corners[0].x = bl.x + crop_left
            self.corners[0].y = bl.y + crop_bottom
            
            self.corners[1].x = tl.x + crop_left
            self.corners[1].y = tl.y - crop_top
            
            self.corners[2].x = tr.x - crop_right
            self.corners[2].y = tr.y - crop_top
            
            self.corners[3].x = br.x - crop_right
            self.corners[3].y = br.y + crop_bottom
        
        self.corners[0] = rotate_point(self.corners[0], angle, origin)
        self.corners[1] = rotate_point(self.corners[1], angle, origin)
        self.corners[2] = rotate_point(self.corners[2], angle, origin)
        self.corners[3] = rotate_point(self.corners[3], angle, origin)
                

    def set_quads(self, context):
        self.corner_quads = []
        
        active_strip = context.scene.sequence_editor.active_strip
        angle = math.radians(active_strip.rotation_start)
        rect_size = 7.5

        for corner in self.corners:
            origin = corner
            
            x1 = corner.x - rect_size
            x2 = corner.x + rect_size
            y1 = corner.y - rect_size
            y2 = corner.y + rect_size
            
            bl = rotate_point(Vector([x1, y1]), angle, origin)
            tl = rotate_point(Vector([x1, y2]), angle, origin)
            tr = rotate_point(Vector([x2, y2]), angle, origin)
            br = rotate_point(Vector([x2, y1]), angle, origin)
            
            self.corner_quads.append([bl, tl, tr, br])

    def modal(self, context, event):
        context.area.tag_redraw()
    
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            mouse_x = event.mouse_region_x
            mouse_y = event.mouse_region_y
            
            self.mouse_pos = Vector([mouse_x, mouse_y])
            self.current_mouse = Vector([mouse_x, mouse_y])
            
            for i in range(len(self.corner_quads)):
                quad = self.corner_quads[i]
                
                bl = quad[0]
                tl = quad[1]
                tr = quad[2]
                br = quad[3]
                
                intersects = intersect_point_quad_2d(
                    self.mouse_pos, bl, tl, tr, br)
            
                if intersects:
                    self.clicked_quad = i
        
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            offset_x, offset_y, fac, preview_zoom = get_preview_offset()
            
            active_strip = context.scene.sequence_editor.active_strip
            angle = math.radians(active_strip.rotation_start)
            
            origin = self.max_corners[2] - self.max_corners[0]

            bl = rotate_point(self.max_corners[0], -angle, origin)
            tl = rotate_point(self.max_corners[1], -angle, origin)
            tr = rotate_point(self.max_corners[2], -angle, origin)
            br = rotate_point(self.max_corners[3], -angle, origin)
            
            bl_current = rotate_point(self.corners[0], -angle, origin)
            tl_current = rotate_point(self.corners[1], -angle, origin)
            tr_current = rotate_point(self.corners[2], -angle, origin)
            br_current = rotate_point(self.corners[3], -angle, origin)
            
            if self.clicked_quad != None:
                for i in range(len(self.corners)):
                    if i == 0:
                        self.crop_left = bl_current.x - bl.x
                        self.crop_left /= preview_zoom * fac
                        
                        self.crop_bottom = bl_current.y - bl.y
                        self.crop_bottom /= preview_zoom * fac
                    elif i == 1:
                        self.crop_left = tl_current.x - tl.x
                        self.crop_left /= preview_zoom * fac
                        
                        self.crop_top = tl.y - tl_current.y
                        self.crop_top /= preview_zoom * fac
                    
                    elif i == 2:
                        self.crop_right = tr.x - tr_current.x
                        self.crop_right /= preview_zoom * fac
                        
                        self.crop_top = tr.y - tr_current.y
                        self.crop_top /= preview_zoom * fac
                    
                    elif i == 3:
                        self.crop_right = br.x - br_current.x
                        self.crop_right /= preview_zoom * fac
                        
                        self.crop_bottom = br_current.y - br.y
                        self.crop_bottom /= preview_zoom * fac
            
            self.clicked_quad = None
            self.mouse_pos = Vector([-1, -1])
            
        elif event.type == 'MOUSEMOVE' and self.clicked_quad != None:
            mouse_x = event.mouse_region_x
            mouse_y = event.mouse_region_y
            self.current_mouse = Vector([mouse_x, mouse_y])
            
        elif event.type in ['MIDDLEMOUSE', 'WHEELDOWNMOUSE', 
                          'WHEELUPMOUSE', 'RIGHT_ARROW', 'LEFT_ARROW']:
            return {'PASS_THROUGH'}
        
        elif event.type in ['C', 'RET', 'NUMPAD_ENTER'] and event.value == 'PRESS':
            offset_x, offset_y, fac, preview_zoom = get_preview_offset()
            
            active_strip = context.scene.sequence_editor.active_strip
            crops = [self.crop_left / self.scale_factor_x, 
                     self.crop_right / self.scale_factor_x,
                     self.crop_bottom / self.scale_factor_y,
                     self.crop_top / self.scale_factor_y,
            ]
            
            self.crop_scale(active_strip, crops)
            
            strip_in = active_strip.input_1
            scene = context.scene
            if scene.tool_settings.use_keyframe_insert_auto:
                cf = context.scene.frame_current
                active_strip.keyframe_insert(data_path='translate_start_x', frame=cf)
                active_strip.keyframe_insert(data_path='translate_start_y', frame=cf)
                active_strip.keyframe_insert(data_path='scale_start_x', frame=cf)
                active_strip.keyframe_insert(data_path='scale_start_y', frame=cf)
                
                strip_in.crop.keyframe_insert(data_path='min_x', frame=cf)
                strip_in.crop.keyframe_insert(data_path='max_x', frame=cf)
                strip_in.crop.keyframe_insert(data_path='min_y', frame=cf)
                strip_in.crop.keyframe_insert(data_path='max_y', frame=cf)
                    
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_crop, 'PREVIEW')
            return {'FINISHED'}
        
        elif (event.alt and event.type =='C') or event.type == 'ESC':
            active_strip = context.scene.sequence_editor.active_strip
            crops = [self.init_crop_left, self.init_crop_right, 
                     self.init_crop_bottom, self.init_crop_top]
            
            self.crop_scale(active_strip, crops)
            
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_crop, 'PREVIEW')
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        scene = context.scene
        
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y
        
        strip = scene.sequence_editor.active_strip
        strip_in = strip.input_1
        
        if not strip_in.use_crop:
            strip_in.use_crop = True
            
            strip_in.crop.min_x = 0
            strip_in.crop.max_x = 0
            strip_in.crop.min_y = 0
            strip_in.crop.max_y = 0
        
        if event.alt:
            self.crop_scale(strip, [0, 0, 0, 0])
            return {'FINISHED'}
        
        self.crop_scale(strip, [0, 0, 0, 0])
        
        args = (self, context)
        self.handle_crop = bpy.types.SpaceSequenceEditor.draw_handler_add(
            draw_callback_px_crop, args, 'PREVIEW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
