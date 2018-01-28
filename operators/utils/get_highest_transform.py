import bpy


def get_tree(strip):
    """
    Recursively ensure all input_1 and input_2 strips are selected
    """
    checked_strips = [strip]

    if hasattr(strip, 'input_1'):
        checked_strips.extend(get_tree(strip.input_1))
    if hasattr(strip, 'input_2'):
        checked_strips.extend(get_tree(strip.input_2))

    return checked_strips


def get_highest_transform(strip):
    """
    Return the highest transform strip in a modifier hierarchy
    
    For example:
    
    Transform
    |__ Input_1
    
    If 'Input_1' strip is selected, this script will return the 
    transform strip.
    
    If no transform is found, it returns the highest strip in the
    hierarchy
    """
    scene = bpy.context.scene
    
    all_sequences = list(sorted(scene.sequence_editor.sequences,
                                key=lambda x: x.channel))
    all_sequences.reverse()
    
    checked_strips = []
    
    for seq in all_sequences:
        if not seq in checked_strips:
            tree = get_tree(seq)
            if strip in tree:
                for branch in tree:
                    if branch.type == "TRANSFORM":
                        return branch
                    elif branch == strip:
                        return seq
            else:
                checked_strips.extend(tree)
