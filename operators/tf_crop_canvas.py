import bpy
import bgl
from mathutils import Vector
from mathutils.geometry import intersect_point_quad_2d

from .tf_utils import get_preview_offset

def draw_callback_crop_canvas(self, context):
    theme = context.user_preferences.themes['Default']
    active_color = theme.view_3d.object_active
    bgl.glColor4f(0.0, 1.0, 1.0, 1.0)
    
    self.set_quads(context)
    
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for corner in self.corners:
        bgl.glVertex2f(corner[0], corner[1])
    bgl.glEnd()

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

class TF_Crop_Canvas(bpy.types.Operator):
    bl_idname = "sequencer.tf_crop_canvas"
    bl_label = "Adjust scene resolution without changing strip sizes"
    bl_options = {'REGISTER', 'UNDO'}
    
    mouse_pos = Vector([-1, -1])
    current_mouse = Vector([-1, -1])
    
    corners = [Vector([-1, -1]), Vector([-1, -1]), Vector([-1, -1]), 
               Vector([-1, -1])]
    max_corners = [Vector([-1, -1]), Vector([-1, -1]), Vector([-1, -1]), 
                   Vector([-1, -1])]
    corner_quads = []
    clicked_quad = -1
    
    handle_crop = None
    
    crop_left = 0
    crop_right = 0
    crop_bottom = 0
    crop_top = 0
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
            context.space_data.type == 'SEQUENCE_EDITOR' and
            context.space_data.view_type == 'PREVIEW' and
            context.space_data.display_mode == 'IMAGE' and 
            len(scene.sequence_editor.sequences) > 0):
            return True
        return False
    
    def set_quads(self, context):
        self.corners = []
        self.corner_quads = []
        
        scene = context.scene
        
        offset_x, offset_y, fac, preview_zoom = get_preview_offset()
        
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y
        
        bl = Vector([0, 0]) * preview_zoom * fac
        bl.x += offset_x
        bl.y += offset_y
        
        tl = Vector([0, res_y]) * preview_zoom * fac
        tl.x += offset_x
        tl.y += offset_y
        
        tr = Vector([res_x, res_y]) * preview_zoom * fac
        tr.x += offset_x
        tr.y += offset_y
        
        br = Vector([res_x, 0]) * preview_zoom * fac
        br.x += offset_x
        br.y += offset_y
        
        self.max_corners = [Vector(bl), Vector(tl), Vector(tr), Vector(br)]
        for corner in self.max_corners:
            corner.x = (corner.x * preview_zoom * fac) + offset_x
            corner.y = (corner.y * preview_zoom * fac) + offset_y
        
        bl = self.max_corners[0]
        tl = self.max_corners[1]
        tr = self.max_corners[2]
        br = self.max_corners[3]
        
        vec = self.current_mouse - self.mouse_pos
        
        crop_left = self.crop_left * preview_zoom * fac
        crop_bottom = self.crop_bottom * preview_zoom * fac
        crop_top = self.crop_top * preview_zoom * fac
        crop_right = self.crop_right * preview_zoom * fac
        
        print('hello')
        
        cushion = 10
        if self.clicked_quad != None:
            for i in range(len(self.max_corners)):
                if self.clicked_quad == 0: # Bottom Left Clicked
                    pt_x = bl.x + vec.x + crop_left
                    pt_y = bl.y + vec.y + crop_bottom
                    pt = Vector(pt_x, pt_y)
                    
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
                    
                
        else:
            self.corners[0].x = bl.x + crop_left
            self.corners[0].y = bl.y + crop_bottom
            
            self.corners[1].x = tl.x + crop_left
            self.corners[1].y = tl.y - crop_top
            
            self.corners[2].x = tr.x - crop_right
            self.corners[2].y = tr.y - crop_top
            
            self.corners[3].x = br.x - crop_right
            self.corners[3].y = br.y + crop_bottom
        
        size = 7.5
        for corner in self.corners:
            bl_x = corner.x - size
            bl_y = corner.y - size
            
            tl_x = corner.x - size
            tl_y = corner.y + size
            
            tr_x = corner.x + size
            tr_y = corner.y + size
            
            br_x = corner.x + size
            br_y = corner.y - size
        
            self.corner_quads.append([
                [bl_x, bl_y],
                [tl_x, tl_y],
                [tr_x, tr_y],
                [br_x, br_y],
            ])
    
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
        
        elif event.type == 'MOUSEMOVE' and self.clicked_quad != None:
            mouse_x = event.mouse_region_x
            mouse_y = event.mouse_region_y
            self.current_mouse = Vector([mouse_x, mouse_y])
        
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            offset_x, offset_y, fac, preview_zoom = get_preview_offset()
            
            bl = self.max_corners[0]
            tl = self.max_corners[1]
            tr = self.max_corners[2]
            br = self.max_corners[3]
            
            bl_current = self.corners[0]
            tl_current = self.corners[1]
            tr_current = self.corners[2]
            br_current = self.corners[3]
            
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
        
        elif ((event.type == 'C' and event.shift and event.value == 'PRESS') or 
               event.type in ['RET', 'NUMPAD_ENTER']):
            bpy.types.SpaceSequenceEditor.draw_handler_remove(
                self.handle_crop, 'PREVIEW')
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        
        
        
        args = (self, context)
        self.handle_crop = bpy.types.SpaceSequenceEditor.draw_handler_add(
            draw_callback_crop_canvas, args, 'PREVIEW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
