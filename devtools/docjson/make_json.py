import os
import json

from .get_operator_tag import get_operator_tag
from .get_operator_docstring import get_operator_docstring
    
def make_shortcuts(idname):
    shortcuts = {
        "vse_transform_tools.select": {
            "0": "keys=Right_Mouse; function=Select Visible Strip",
            "1": "keys=Shift; function=Enable Multi Selection",
            "2": "keys=A; function=Toggle Selection",
        },
        "vse_transform_tools.add_transform": {
            "0": "keys=T"
        },
        "vse_transform_tools.grab": {
            "0": "keys=G; function=Begin Moving, Add Transform if Needed",
            "1": "keys=Shift; function=Hold to Enable Fine Tuning",
            "2": "keys=Ctrl; function=Hold to Enable Snapping",
            "3": "keys=Right_Mouse; function=Escape Grab Mode",
            "4": "keys=Esc; function=Escape Grab Mode",
            "5": "keys=Left_Mouse; function=Set Position, End Grab Mode",
            "6": "keys=Enter; function=Set Position, End Grab Mode",
            "7": "keys=0 1 2 3 4 5 6 7 8 9 .; function=Set Position by Value Entered",
            "8": "keys=X Y; function=Constrain Grabbing to Respective Axis",
            "9": "keys=Middle_Mouse_Button; function=Constrain Grabbing to Axis",
            "10": "keys=Alt G; function=Set Position to [0, 0]",
        },
        "vse_transform_tools.scale": {
            "0": "keys=S; function=Begin Scaling, Add Transform if Needed",
            "1": "keys=Shift; function=Enable Fine Tuning",
            "2": "keys=Ctrl; function=Enable Stepwise scaling",
            "3": "keys=Right_Mouse; function=Escape Scale Mode",
            "4": "keys=Esc; function=Escape Scale Mode",
            "5": "keys=Left_Mouse; function=Set Scale, End Scale Mode",
            "6": "keys=Enter; function=Set Scale, End Scale Mode",
            "7": "keys=0 1 2 3 4 5 6 7 8 9 .; function=Set Scale by Value Entered",
            "8": "keys=X Y; function=Constrain Scaling to Respective Axis",
            "9": "keys=Middle_Mouse_Button; function=Constrain Scaling to Axis",
            "10": "keys=Alt S; function=Unscale",
        },
        "vse_transform_tools.rotate": {
            "0": "keys=R; function=Begin Rotating, Add Transform if Needed",
            "1": "keys=Shift; function=Hold to Enable Fine Tuning",
            "2": "keys=Ctrl; function=Hold to Enable Stepwise Rotation",
            "3": "keys=Right_Mouse; function=Escape Rotate Mode",
            "4": "keys=Esc; function=Escape Rotate Mode",
            "5": "keys=Left_Mouse; function=Set Rotation, End Rotate Mode",
            "6": "keys=Enter; function=Set Rotation, End Rotate Mode",
            "7": "keys=0 1 2 3 4 5 6 7 8 9 .; function=Set Rotation to Value Entered",
            "8": "keys=Alt R; function=Set Rotation to 0 Degrees",
        },
        "vse_transform_tools.adjust_alpha": {
            "0": "keys=Q; function=Begin Alpha Adjusting",
            "1": "keys=Ctrl; function=Round to Nearest Tenth",
            "2": "keys=Right_Mouse; function=Escape Alpha Adjust Mode",
            "4": "keys=Esc; function=Escape Alpha Adjust Mode",
            "5": "keys=Left_Mouse; function=Set Alpha, End Alpha Adjust Mode",
            "6": "keys=Enter; function=Set Alpha, End Alpha Adjust Mode",
            "7": "keys=0 1 2 3 4 5 6 7 8 9 .; function=Set Alpha to Value Entered",
            "8": "keys=Alt Q; function=Set Alpha to 1.0",
        },
        "vse_transform_tools.crop": {
            "0": "keys=C; function=Begin/Set Cropping, Add Transform if Needed",
            "1": "keys=Esc; function=Escape Crop Mode",
            "2": "keys=Left_Mouse; function=Click Handles to Drag",
            "3": "keys=Enter; function=Set Crop, End Grab Mode",
            "4": "keys=Alt C; function=Uncrop",
        },
        "vse_transform_tools.autocrop": {
            "0": "keys=Shift C"
        },
        "vse_transform_tools.call_menu": {
            "0": "keys=I"
        },
        "vse_transform_tools.increment_pivot": {
            "0": "keys=Period"
        },
        "vse_transform_tools.decrement_pivot": {
            "0": "keys=Comma"
        },
        "vse_transform_tools.duplicate": {
            "0": "keys=Shift D"
        },
        "vse_transform_tools.delete": {
            "0": "keys=Del"
        },
        "vse_transform_tools.meta_toggle": {
            "0": "keys=Tab"
        },
        "vse_transform_tools.set_cursor2d": {
            "0": "keys=Left_Mouse"
        },
    }

    return shortcuts[idname]


def make_json(ops_path, output_path=None):
    """
    Make a JSON out of all the data we gather about the operators
    """
    
    info = {}
    
    for file in sorted(os.listdir(ops_path)):
        if file.endswith('.py') and not file.startswith('_'):
            filepath = os.path.join(ops_path, file)
            
            idname = get_operator_tag(filepath, "bl_idname")
            label = get_operator_tag(filepath, "bl_label")
            description = get_operator_tag(filepath, "bl_description")
            docstring = get_operator_docstring(filepath)
            shortcuts = make_shortcuts(idname)
            
            info[idname] = {}
            info[idname]["label"] = label
            info[idname]["description"] = description
            info[idname]["docstring"] = docstring
            info[idname]["shortcuts"] = shortcuts
    
    if output_path:
        text = json.dumps(info, indent=4, sort_keys=True)
        with open(output_path, 'w') as f:
            f.write(text)
    
    return info
