import bpy

LAST_OP_LEN = 0

def print_history(history):
    s = ""
    s += "HISTORY\n"
    for group in history:
        s += "_GROUP\n"
        for item in group:
            s += "__" + item.name + "\n"
    return s

def fix_histories(scene: bpy.types.Scene):
    if "histories" not in scene:
        return
    histories = scene["histories"]
    print("Fixing Histories::Before: ", print_history(histories))
    new_histories = []
    for group in histories:
        new_group = list(filter(lambda a: a is not None, group))
        if any(x.name in scene.objects for x in new_group):
            new_histories.append(new_group)
    new_histories = list(filter(lambda a: a != [], new_histories))
    print("Fixing Histories::After: ", print_history(new_histories))
    scene["histories"] = new_histories


def delete_post(scene: bpy.types.Scene):
    fix_histories(scene)


def operator_post(scene: bpy.types.Scene, OP: bpy.types.Operator):
    print("*************", OP.bl_idname, "*************")
    if OP.bl_idname in ['OBJECT_OT_delete', 'OUTLINER_OT_delete']:
        delete_post(scene)


def redo_post(scene, _):
    fix_histories(scene)


def depsgraph_update_post(scene, depsgraph):
    global LAST_OP_LEN
    OPERATORS = bpy.context.window_manager.operators
    if len(OPERATORS) == LAST_OP_LEN or len(OPERATORS) == 0:
        return
    LAST_OP_LEN = len(OPERATORS)
    OP = OPERATORS[-1]
    operator_post(scene, OP)


def register():
    bpy.app.handlers.depsgraph_update_post.append(depsgraph_update_post)
    bpy.app.handlers.redo_post.append(redo_post)


def unregister():
    try:
        bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update_post)
    except ValueError as _:
        pass

    try:
        bpy.app.handlers.redo_post.remove(redo_post)
    except ValueError as _:
        pass
