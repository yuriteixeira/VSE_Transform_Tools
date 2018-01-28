import bpy


class CallMenu(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/9Cx6XKj.gif)
    
    You may also enable automatic keyframe insertion.
    
    ![Automatic Keyframe Insertion](https://i.imgur.com/kFtT1ja.jpg)
    """
    bl_idname = "vse_transform_tools.call_menu"
    bl_label = "Call Menu"
    bl_description = "Open keyframe insertion menu"

    @classmethod
    def poll(cls, context):
        if (context.scene.sequence_editor and
           context.space_data.type == 'SEQUENCE_EDITOR' and
           context.region.type == 'PREVIEW'):
            return True
        return False

    def execute(self, context):
        bpy.ops.wm.call_menu(name="VSE_MT_Insert_keyframe_Menu")
        return {'FINISHED'}


class MenuInsertKeyframe(bpy.types.Menu):
    bl_label = "Insert KeyFrame Menu"
    bl_idname = "VSE_MT_Insert_keyframe_Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("vse_transform_tools.insert_keyframe",  text="Location").ch = (1,0,0,0,0)
        layout.operator("vse_transform_tools.insert_keyframe",  text="Rotation").ch = (0,1,0,0,0)
        layout.operator("vse_transform_tools.insert_keyframe", text="Scale").ch = (0,0,1,0,0)
        layout.operator("vse_transform_tools.insert_keyframe", text="LocRot").ch = (1,1,0,0,0)
        layout.operator("vse_transform_tools.insert_keyframe", text="LocScale").ch =(1,0,1,0,0)
        layout.operator("vse_transform_tools.insert_keyframe", text="RotScale").ch = (0,1,1,0,0)
        layout.operator("vse_transform_tools.insert_keyframe", text="LocRotScale").ch = (1,1,1,0,0)
        layout.separator()
        layout.operator("vse_transform_tools.insert_keyframe", text="Alpha").ch = (0,0,0,1,0)
        layout.separator()
        layout.operator("vse_transform_tools.insert_keyframe", text="CropScale").ch = (0,0,1,0,1)
        layout.separator()
        layout.operator("vse_transform_tools.insert_keyframe", text="All").ch = (1,1,1,1,1)


class InsertKeyframe(bpy.types.Operator):
    bl_idname = "vse_transform_tools.insert_keyframe"
    bl_label = "Transform Insert KeyFrame"
    bl_options = {'REGISTER', 'UNDO'}

    ch = bpy.props.IntVectorProperty(name="ch", default=(0, 0, 0, 0, 0), size=5)

    @classmethod
    def poll(cls, context):
        ret = False
        if context.scene.sequence_editor:
            ret = True
        return ret and context.space_data.type == 'SEQUENCE_EDITOR'

    def execute(self, context):
        cf = context.scene.frame_current

        for seq in context.scene.sequence_editor.sequences:
            if seq.select and seq.type == 'TRANSFORM':
                if self.ch[0] == 1:
                    seq.keyframe_insert(data_path="translate_start_x", frame=cf)
                    seq.keyframe_insert(data_path="translate_start_y", frame=cf)
                if self.ch[1] == 1:
                    seq.keyframe_insert(data_path="rotation_start", frame=cf)
                if self.ch[2] == 1:
                    seq.keyframe_insert(data_path="scale_start_x", frame=cf)
                    seq.keyframe_insert(data_path="scale_start_y", frame=cf)
                if self.ch[3] == 1:
                    seq.keyframe_insert(data_path="blend_alpha", frame=cf)
                if self.ch[4] == 1 and seq.input_1.use_crop:
                    seq.input_1.crop.keyframe_insert(data_path="min_x", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="max_x", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="min_y", frame=cf)
                    seq.input_1.crop.keyframe_insert(data_path="max_y", frame=cf)

        return {'FINISHED'}
