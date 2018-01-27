from .clear_rejects import clear_rejects

def get_transform_strips(strips):
    '''Get a list of transform strips'''
    rejects = []
    for strip in strips:
        if not strip.type == 'TRANSFORM':
            rejects.append(strip)
        #elif strip.input_1.type == 'TRANSFORM':
        #    rejects.append(strip.input_1)
    return clear_rejects(strips, rejects)