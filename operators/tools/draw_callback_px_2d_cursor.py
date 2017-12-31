def draw_callback_px_2d_cursor(self, context):
    c2d = context.region.view2d.view_to_region(context.scene.seq_cursor2d_loc[0],context.scene.seq_cursor2d_loc[1],clip=False)

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glColor4f(0.7, 0.7, 0.7, 1.0)
    bgl.glPushMatrix()          
    bgl.glTranslatef(c2d[0],c2d[1],0)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2i(0, -15)   
    bgl.glVertex2i(0, -5)    
    bgl.glVertex2i(0, 15)
    bgl.glVertex2i(0, 5)
    bgl.glVertex2i(-15, 0)   
    bgl.glVertex2i(-5, 0)
    bgl.glVertex2i(15, 0)    
    bgl.glVertex2i(5, 0)
    bgl.glEnd()
    
    size = 10
    c = []
    s = []
    for i in range(16):
        c.append(cos(i*pi/8))
        s.append(sin(i*pi/8)) 
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for i in range(16):
        bgl.glVertex2f(size*c[i], size*s[i])         
    bgl.glEnd()
    
    bgl.glEnable(bgl.GL_LINE_STIPPLE)
    bgl.glLineStipple(4, 0x5555)
    bgl.glColor4f(1.0, 0.0, 0.0, 1.0)
    
    bgl.glBegin(bgl.GL_LINE_LOOP)
    for i in range(16):
        bgl.glVertex2f(size*c[i], size*s[i])         
    bgl.glEnd()
    
    bgl.glPopMatrix()
    
    bgl.glDisable(bgl.GL_LINE_STIPPLE)            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
