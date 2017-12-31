import bgl

def draw_callback_px_select(self, context):
    bgl.glEnable(bgl.GL_BLEND)
    col_act = context.user_preferences.themes['Default'].view_3d.object_active
    col_sel = context.user_preferences.themes['Default'].view_3d.object_selected
    act_seq = context.scene.sequence_editor.active_strip
    bgl.glLineWidth(4)
    
    for seq, quad in self.quad_list:
        if seq.select:
            bgl.glColor4f(col_sel[0], col_sel[1], col_sel[2], 0.9-self.t/20)
            if seq == context.scene.sequence_editor.active_strip:
                bgl.glColor4f(col_act[0], col_act[1], col_act[2], 0.9-self.t/20)
                
            bgl.glBegin(bgl.GL_LINE_LOOP)
            for vec in quad:
                pos = context.region.view2d.view_to_region(vec.x,vec.y, clip=False)
                bgl.glVertex2i(pos[0], pos[1])   
            bgl.glEnd()
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
