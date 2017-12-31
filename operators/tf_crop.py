import bpy
import bgl

import math
import mathutils

from .tools.crop_scale import crop_scale, crop_scale2

vec_bl = mathutils.Vector((0,0))
vec_tr = mathutils.Vector((0,0))
origin = [10000,10000]
image_size = 200
fframe = 0

def draw_callback_px_crop(self, context):
    parent_seq =  context.scene.sequence_editor.active_strip
    active_seq = parent_seq.input_1

    global image_size, origin, vec_bl, vec_tr, vec_ct
    image_fac = 2*image_size/active_seq.elements[0].orig_width
    fac  = active_seq.elements[0].orig_height/active_seq.elements[0].orig_width
    vec_bl = mathutils.Vector((origin[0]-image_size + active_seq.crop.min_x*image_fac,origin[1]-image_size*fac + active_seq.crop.min_y*image_fac))
    vec_tr = mathutils.Vector((origin[0]+image_size - active_seq.crop.max_x*image_fac,origin[1] + image_size*fac - active_seq.crop.max_y*image_fac))
    vec_ct = (vec_bl + (vec_tr- vec_bl)/2)

    #Init
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    bgl.glEnable(bgl.GL_TEXTURE_2D)
    bgl.glEnable(bgl.GL_DEPTH_TEST)

    #Texture
    texture1 = self.img.bindcode
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture1[0]);
    bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
    bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)

    bgl.glPushMatrix()
    bgl.glTranslatef(origin[0],origin[1],0)
    bgl.glBegin(bgl.GL_QUADS)
    bgl.glTexCoord2d(0,0)
    bgl.glVertex2f(-image_size, -image_size*fac)
    bgl.glTexCoord2d(0,1)
    bgl.glVertex2f(-image_size , image_size*fac)
    bgl.glTexCoord2d(1,1)
    bgl.glVertex2f(image_size , image_size*fac)
    bgl.glTexCoord2d(1,0)
    bgl.glVertex2f(image_size , -image_size*fac)
    bgl.glEnd()
    bgl.glDisable(bgl.GL_TEXTURE_2D)

    #Cadre
    bgl.glLineWidth(2)
    bgl.glColor4f(0.0, 1.0, 1.0, 1.0)

    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex2f(-image_size + active_seq.crop.min_x*image_fac, -image_size*fac + active_seq.crop.min_y*image_fac)
    bgl.glVertex2f(-image_size + active_seq.crop.min_x*image_fac, image_size*fac - active_seq.crop.max_y*image_fac)
    bgl.glVertex2f(image_size - active_seq.crop.max_x*image_fac, image_size*fac - active_seq.crop.max_y*image_fac)
    bgl.glVertex2f(image_size - active_seq.crop.max_x*image_fac, -image_size*fac + active_seq.crop.min_y*image_fac)
    bgl.glEnd()

    #Point
    bgl.glEnable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(15)

    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(-image_size + active_seq.crop.min_x*image_fac, -image_size*fac + active_seq.crop.min_y*image_fac)
    bgl.glVertex2f(image_size - active_seq.crop.max_x*image_fac, image_size*fac - active_seq.crop.max_y*image_fac)
    #bgl.glVertex2f(vec_ct.x-origin[0],vec_ct.y-origin[1])
    bgl.glEnd()
    bgl.glPopMatrix()
    for i in range(4):
        bgl.glPushMatrix()
        bgl.glTranslatef(vec_ct.x,vec_ct.y,0)
        bgl.glRotatef(i*90,0,0,1)
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(0,0)
        bgl.glVertex2f(10, 0)
        bgl.glEnd()

        bgl.glPopMatrix()
        
    bgl.glEnable(bgl.GL_POINT_SMOOTH)
    bgl.glPointSize(1)
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

class TF_Crop(bpy.types.Operator):
    bl_idname = "sequencer.tf_crop"
    bl_label = "Draw the crop"
    bl_options = {'REGISTER', 'UNDO'}

    _handle_crop = None
    sel_point = 0
    mmb = False

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            if context.scene.sequence_editor.active_strip:
                if context.scene.sequence_editor.active_strip.type == 'TRANSFORM':
                    if context.scene.sequence_editor.active_strip.select:
                        if context.scene.sequence_editor.active_strip.input_1.type in ['MOVIE','IMAGE']:
                            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW'

    def modal(self, context, event):
        context.area.tag_redraw()
        seq = context.scene.sequence_editor.active_strip
        active_seq = context.scene.sequence_editor.active_strip.input_1
        global image_size, fframe
        self.pos_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))

        if self.enter_modal:
            self.img.reload()
            self.enter_modal = False
        #move fram
        if event.type in ['RIGHT_ARROW','LEFT_ARROW']:
            if event.type == 'RIGHT_ARROW' and event.value == 'PRESS':
                context.scene.frame_current +=1
                fframe = fframe + 1
            if event.type == 'LEFT_ARROW' and event.value == 'PRESS':
                context.scene.frame_current -=1
                fframe = fframe - 1
            if seq.input_1.type == 'MOVIE' and event.value == 'RELEASE':
                self.img.reload()
            if seq.input_1.type == 'IMAGE' and event.value == 'RELEASE':
                if len(seq.input_1.elements) == 1:
                    index = 0
                else:
                    index = context.scene.frame_current - seq.frame_start + seq.input_1.frame_offset_start
                    if index < seq.input_1.frame_offset_start:
                        index = seq.input_1.frame_offset_start
                    if index > seq.input_1.frame_final_duration + seq.input_1.frame_offset_start - 1:
                        index = seq.input_1.frame_final_duration + seq.input_1.frame_offset_start - 1

                self.img.user_clear()
                bpy.data.images.remove(self.img)
                name = seq.input_1.elements[index].filename
                dir = seq.input_1.directory
                fp = dir+name
                self.img = bpy.data.images.load(fp)
        ret = self.img.gl_load(fframe, bgl.GL_NEAREST, bgl.GL_NEAREST)

        #zoom image
        if event.type in ['WHEELDOWNMOUSE','WHEELUPMOUSE']:
            if event.type =='WHEELDOWNMOUSE':
                image_size -=10
            if event.type =='WHEELUPMOUSE':
                image_size +=10

        #select a corner
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            len_bl = self.pos_mouse - vec_bl
            len_tr = self.pos_mouse - vec_tr
            len_org = self.pos_mouse - vec_ct
            if len_bl.length < 7.5:
                self.sel_point = 1
                self.init_min_x = active_seq.crop.min_x
                self.init_min_y = active_seq.crop.min_y

            elif len_tr.length < 7.5:
                self.sel_point = 2
                self.init_max_x = active_seq.crop.max_x
                self.init_max_y = active_seq.crop.max_y

            elif len_org.length < 7.5:
                self.sel_point = 3
                self.init_min_x = active_seq.crop.min_x
                self.init_min_y = active_seq.crop.min_y
                self.init_max_x = active_seq.crop.max_x
                self.init_max_y = active_seq.crop.max_y
            else:
                self.sel_point = 0

            #init for scaling the strip according to the crop
            self.first_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))
            self.org_w = active_seq.elements[0].orig_width
            self.org_h = active_seq.elements[0].orig_height
            self.ratio_org = self.org_h/self.org_w
            crop_x = self.org_w - (active_seq.crop.min_x + active_seq.crop.max_x)
            crop_y = self.org_h - (active_seq.crop.min_y + active_seq.crop.max_y)

            self.fac_init = max(seq.scale_start_x,seq.scale_start_y)

        #crop
        if event.type == 'MOUSEMOVE' and self.sel_point != 0:
            limit = 50
            vec_act = (self.pos_mouse - self.first_mouse)/(2*image_size)
            step_x = self.org_w*vec_act.x
            step_y = self.org_h*vec_act.y/self.ratio_org
            if self.sel_point == 1:
                active_seq.crop.min_x = self.init_min_x + step_x
                active_seq.crop.min_y = self.init_min_y + step_y
            if self.sel_point == 2:
                active_seq.crop.max_x = self.init_max_x - step_x
                active_seq.crop.max_y = self.init_max_y - step_y
            if self.sel_point == 3:
                active_seq.crop.min_x = self.init_min_x + step_x
                active_seq.crop.min_y = self.init_min_y + step_y
                active_seq.crop.max_x = self.init_max_x - step_x
                active_seq.crop.max_y = self.init_max_y - step_y

            #scale the strip according to the crop
            if not active_seq.use_translation:
                crop_scale2(seq, self.fac_init)

        #move the image
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.sel_point = 0

        if event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
            self.mmb = True
            self.first_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))

        if event.type == 'MOUSEMOVE' and self.mmb:
            vec_act = mathutils.Vector((event.mouse_region_x,event.mouse_region_y)) - self.first_mouse
            global origin
            origin = [origin[0]+vec_act.x,origin[1]+vec_act.y]
            self.first_mouse = mathutils.Vector((event.mouse_region_x,event.mouse_region_y))

        if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
            self.mmb = False
        #keyframe
        if event.type == 'I':
            bpy.ops.sequencer.tf_call_menu('INVOKE_DEFAULT')
        #clear the crop inside the modal
        if event.alt and event.type =='C':
            seq.input_1.crop.min_x = seq.input_1.crop.min_y = 0
            seq.input_1.crop.max_x = seq.input_1.crop.max_y = 0
            crop_scale(seq,max(seq.scale_start_x,seq.scale_start_y))
        #close
        if event.type == 'C' and event.value == 'PRESS':
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle_crop, 'PREVIEW')
            if active_seq.type in ['MOVIE','IMAGE']:
                self.img.user_clear()
                bpy.data.images.remove(self.img)

            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        seq = context.scene.sequence_editor.active_strip
        if event.alt :
            seq.input_1.crop.min_x = seq.input_1.crop.min_y = 0
            seq.input_1.crop.max_x = seq.input_1.crop.max_y = 0
            crop_scale(seq,max(seq.scale_start_x,seq.scale_start_y))
            ret = 'FINISHED'
        else:
            global origin, fframe
            if origin == [10000,10000]:
                origin = context.region.view2d.view_to_region(0,0,clip=False)

            if seq.input_1.type == 'MOVIE':
                fp = seq.input_1.filepath
                self.img = bpy.data.images.load(fp)
                fframe = -seq.frame_start  + seq.input_1.frame_offset_start + context.scene.frame_current + 1
                self.enter_modal = True

            if seq.input_1.type == 'IMAGE':
                if len(seq.input_1.elements) == 1:
                    index = 0
                else:
                    index = context.scene.frame_current - seq.frame_start + seq.input_1.frame_offset_start
                    if index < seq.input_1.frame_offset_start:
                        index = seq.input_1.frame_offset_start
                    if index > seq.input_1.frame_final_duration + seq.input_1.frame_offset_start - 1:
                        index = seq.input_1.frame_final_duration + seq.input_1.frame_offset_start - 1

                name = seq.input_1.elements[index].filename
                dir = seq.input_1.directory
                fp = dir+name
                self.img = bpy.data.images.load(fp)
                self.enter_modal = False

            args = (self, context)
            self._handle_crop = bpy.types.SpaceSequenceEditor.draw_handler_add(draw_callback_px_crop, args, 'PREVIEW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            ret = 'RUNNING_MODAL'

        return {ret}
