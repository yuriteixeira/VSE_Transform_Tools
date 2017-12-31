import bpy
import mathutils

from .tools.make_quad import make_quad

class TF_Select(bpy.types.Operator):
    bl_idname = "sequencer.tf_select"
    bl_label = "Select Transform Sequence"
    
    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR' and context.region.type == 'PREVIEW' 
                
    def invoke(self, context, event):
        
        pos = context.region.view2d.region_to_view(event.mouse_region_x,event.mouse_region_y)
        po = mathutils.Vector((pos[0],pos[1]))
        list_sel = []
        
        fc = context.scene.frame_current
        for seq in reversed(context.scene.sequence_editor.sequences):
            if seq.type == 'TRANSFORM' and not seq.mute:    
                p0,p1,p2,p3 = make_quad(seq)                     
                if not event.type == 'A':
                    if mathutils.geometry.intersect_point_quad_2d(po, p0, p1, p2, p3) and seq.frame_start <= fc and (seq.frame_start + seq.frame_final_duration) >= fc:
                        list_sel.append(seq)
                        if not event.shift :
                            bpy.ops.sequencer.select_all(action='DESELECT')
                            seq.select = True
                            bpy.context.scene.sequence_editor.active_strip = seq
                            break
                        else :
                            if not seq.select:
                                seq.select = True
                                bpy.context.scene.sequence_editor.active_strip = seq
                                break
                            else:
                                seq.select = False
                                break
        if not list_sel and not event.shift and not event.type == 'A':
            bpy.ops.sequencer.select_all(action='DESELECT')
            
        if event.type == 'A':
            temp_sel = False
            for seq in reversed(context.scene.sequence_editor.sequences):
                if seq.select:
                    temp_sel = True     
                if seq.type == 'TRANSFORM' and seq.frame_start <= fc and (seq.frame_start + seq.frame_final_duration) >= fc:
                    seq.select = True
            if temp_sel == True:
                bpy.ops.sequencer.select_all(action='DESELECT')       
            
        bpy.ops.sequencer.tf_draw_selection('INVOKE_DEFAULT') 
        return {'FINISHED'}
