import bgl


def draw_snap(self, loc, orientation):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    bgl.glPushMatrix()
    
    if orientation == "VERTICAL":
        bgl.glTranslatef(loc, 0, 0)
        
        bgl.glBegin(bgl.GL_LINES)
        bgl.glColor4f(1.0, 0.0, 1.0, 0.25)
        bgl.glVertex2f(0, -10000)
        bgl.glVertex2f(0, 10000)
        bgl.glEnd()
    elif orientation == "HORIZONTAL":
        bgl.glTranslatef(0, loc, 0)
    
        bgl.glBegin(bgl.GL_LINES)
        bgl.glColor4f(1.0, 0.0, 1.0, 0.25)
        bgl.glVertex2f(-10000, 0)
        bgl.glVertex2f(10000, 0)
        bgl.glEnd()
    
    bgl.glPopMatrix()
    
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
