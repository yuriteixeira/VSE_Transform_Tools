from .clear_rejects import clear_rejects

def get_nontransformed_strips(strips):
    '''
    Generate a list strips without a transform modifier
    '''
    rejects = []
    for strip in strips:
        if strip.type == 'SOUND':
            rejects.append(strip)
        if strip.type == 'TRANSFORM':
            rejects.append(strip)
            rejects.append(strip.input_1)
    return clear_rejects(strips, rejects)