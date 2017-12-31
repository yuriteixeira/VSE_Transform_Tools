import bpy

def crop_scale(seq, fac_init):
    seq_in = seq.input_1
    len_crop_x = seq_in.elements[0].orig_width - (seq_in.crop.min_x + seq_in.crop.max_x)
    len_crop_y = seq_in.elements[0].orig_height - (seq_in.crop.min_y + seq_in.crop.max_y)
    res_x = bpy.context.scene.render.resolution_x
    res_y = bpy.context.scene.render.resolution_y
    ratio_x = len_crop_x/res_x
    ratio_y = len_crop_y/res_y
    ratio_x = 0.00001 if ratio_x == 0 else ratio_x
    ratio_y = 0.00001 if ratio_y == 0 else ratio_y
    if ratio_x > ratio_y:
        ratio_y *= fac_init/ratio_x
        ratio_x = fac_init
    else:
        ratio_x *= fac_init/ratio_y
        ratio_y = fac_init

    seq.scale_start_x = ratio_x
    seq.scale_start_y = ratio_y

def crop_scale2(seq, fac_init):
    '''For cropping videos in place'''
    seq_in = seq.input_1
    len_crop_x = seq_in.elements[0].orig_width - (seq_in.crop.min_x + seq_in.crop.max_x)
    len_crop_y = seq_in.elements[0].orig_height - (seq_in.crop.min_y + seq_in.crop.max_y)
    res_x = bpy.context.scene.render.resolution_x
    res_y = bpy.context.scene.render.resolution_y

    seq.scale_start_x = len_crop_x / res_x
    seq.scale_start_y = len_crop_y / res_y
    
    seq.translate_start_x = (((seq_in.crop.min_x / res_x) / 2) * 100) - (((seq_in.crop.max_x / res_x) / 2) * 100)
    seq.translate_start_y = (((seq_in.crop.min_y / res_y) / 2) * 100) - (((seq_in.crop.max_y / res_y) / 2) * 100)
