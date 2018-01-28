import bpy
from operator import attrgetter
from .utils import get_children


def get_vertical_translation(strips):
    """
    Determine how many channels up the strips need to be moved
    in order to accomodate them all
    """
    scene = bpy.context.scene

    min_channel = min(strips, key=attrgetter('channel')).channel
    max_channel = max(strips, key=attrgetter('channel')).channel

    channel_count = (max_channel - min_channel) + 1

    frame_start = min(strips, key=attrgetter('frame_start')).frame_start
    frame_end = max(strips, key=attrgetter('frame_final_end')).frame_final_end

    all_sequences = list(sorted(scene.sequence_editor.sequences,
                                key=lambda x: x.frame_start))

    blocked_channels = []
    for seq in all_sequences:
        if (seq not in strips and
                seq.frame_start <= frame_end and
                seq.frame_final_end >= frame_start):
            blocked_channels.append(seq.channel)
        elif seq.frame_start > frame_end:
            break

    i = max_channel + 1
    while True:
        for x in range(i, i + channel_count):
            conflict = False
            if x in blocked_channels:
                conflict = True
                break
        if not conflict:
            return x - max_channel
        i += 1


class Duplicate(bpy.types.Operator):
    bl_idname = "vse_transform_tools.duplicate"
    bl_label = "Duplicate"
    bl_options = {'REGISTER', 'UNDO'}

    called_grab = False

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
           scene.sequence_editor.active_strip):
            return True
        return False

    def invoke(self, context, event):

        selected = context.selected_sequences

        duplicated = []

        for strip in selected:
            if strip not in duplicated:
                bpy.ops.sequencer.select_all(action="DESELECT")

                duplicated.extend(get_children(strip, select=True))
                vertical_translation = get_vertical_translation(
                    context.selected_sequences)

                bpy.ops.sequencer.duplicate_move(
                        SEQUENCER_OT_duplicate={"mode": "TRANSLATION"},
                        TRANSFORM_OT_seq_slide={
                            "value": (0, vertical_translation)})

        return bpy.ops.vse_transform_tools.grab('INVOKE_DEFAULT')
