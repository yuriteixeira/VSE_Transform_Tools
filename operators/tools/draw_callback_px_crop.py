import bgl
import mathutils

def draw_callback_px_crop(self, context):
    active_seq = context.scene.sequence_editor.active_strip.input_1
             
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
