def keymap():
    """
    The hotkeys used by VSE_Transform_Tools

    Returns
    -------
    keymap_dict: dictionary
        The heirarchy is formatted like this:

            Group Name
                Space Type
                    Region Type
                        Operator ID Name
                            hotkey_id : ["type=A", shift="True", ...]
    """

    keymap_dict = {
        "SequencerPreview": {
            "SEQUENCE_EDITOR": {
                "WINDOW": {
                    "vse_transform_tools.add_transform": {
                        "0": ["type=T"]
                    },
                    "vse_transform_tools.adjust_alpha": {
                        "0": ["type=Q"],
                        "1": ["type=Q", "alt=True"],
                    },
                    "vse_transform_tools.autocrop": {
                        "0": ["type=C", "shift=True"]
                    },
                    "vse_transform_tools.scale": {
                        "0": ["type=S"],
                        "1": ["type=S", "alt=True"]
                    },
                    "vse_transform_tools.crop": {
                        "0": ["type=C"],
                        "1": ["type=C", "alt=True"]
                    },
                    "vse_transform_tools.grab": {
                        "0": ["type=G"],
                        "1": ["type=G", "alt=True"]
                    },
                    "vse_transform_tools.duplicate": {
                        "0": ["type=D", "shift=True"]
                    },
                    "vse_transform_tools.rotate": {
                        "0": ["type=R"],
                        "1": ["type=R", "alt=True"]
                    },
                    "vse_transform_tools.call_menu": {
                        "0": ["type=I"]
                    },
                    "vse_transform_tools.delete": {
                        "0": ["type=DEL"]
                    },
                    "vse_transform_tools.meta_toggle": {
                        "0": ["type=TAB"]
                    },
                    "vse_transform_tools.select": {
                        "0": ["type=RIGHTMOUSE"],
                        "1": ["type=RIGHTMOUSE", "shift=True"],
                        "2": ["type=A"]
                    },
                    "vse_transform_tools.set_cursor2d": {
                        "0": ["type=LEFTMOUSE"],
                        "1": ["type=LEFTMOUSE", "ctrl=True"]
                    }
                }
            }
        }
    }
    return keymap_dict
