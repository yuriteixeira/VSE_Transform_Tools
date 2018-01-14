def clear_rejects(strips, rejects):
    '''Remove rejects from strips'''
    strips = list(strips)
    i = 0
    while i < len(strips):
        if strips[i] in rejects:
            strips.pop(i)
        else:
            i += 1
    return strips
