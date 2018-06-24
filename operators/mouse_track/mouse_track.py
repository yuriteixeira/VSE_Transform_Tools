import bpy
from mathutils import Vector

from ..utils.geometry import  mouse_to_res

class MouseTrack(bpy.types.Operator):
    """
    Track mouse position and apply as keyframes to a transform modifier
    """
    bl_idname = "vse_transform_tools.mouse_track"
    bl_label = "Mouse Track"
    bl_description = "Track mouse position and apply as keyframes to a transform modifier"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
                scene.sequence_editor.active_strip and
                scene.sequence_editor.active_strip.type == "TRANSFORM"):
            return True
        return False

    def modal(self, context, event):
        scene = context.scene

        strip = scene.sequence_editor.active_strip

        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y

        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y

        mouse_vec = Vector([mouse_x, mouse_y])
        mouse_pos = mouse_to_res(mouse_vec)

        if strip.translation_unit == 'PERCENT':
            x = ((mouse_pos.x * 100) / res_x) - 50
            y = ((mouse_pos.y * 100) / res_y) - 50
        else:
            x = mouse_pos.x - (res_x / 2)
            y = mouse_pos.y - (res_y / 2)

        strip.translate_start_x = x
        strip.translate_start_y = y

        strip.keyframe_insert(
            data_path="translate_start_x", frame=scene.frame_current)
        strip.keyframe_insert(
            data_path="translate_start_y", frame=scene.frame_current)

        if event.type == 'M' and event.value == 'RELEASE':
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_frame = context.scene.frame_current
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
