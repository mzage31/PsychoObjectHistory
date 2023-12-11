import bpy
import idprop
from . import pv_utils

HISTORY_COPY_OBJECT = None
HISTORY_COPY_IS_CUT = False


class OP_InitializeObjectHistory(bpy.types.Operator):
    bl_idname = "object.initialize_object_history"
    bl_label = "Initialize Object History"
    bl_description = "Initializes object history for the active object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        if "histories" not in context.scene:
            context.scene["histories"] = [[context.object]]
        else:
            histories = context.scene["histories"]
            if isinstance(histories, idprop.types.IDPropertyArray):
                histories = histories.to_list()
            histories.append([context.object])
            context.scene["histories"] = histories
        return {'FINISHED'}


class OP_DeleteAllObjectHistory(bpy.types.Operator):
    bl_idname = "object.delete_object_history"
    bl_label = "Delete Object History"
    bl_description = "Deletes / Uninitializes all history for the active object. Retains active history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "histories" in context.scene

    def execute(self, context):
        obj = context.active_object
        histories = context.scene["histories"]
        g = None
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    g = history_group
        if g is not None:
            histories.remove(g)
        context.scene["histories"] = histories
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class OP_DuplicateObjectHistory(bpy.types.Operator):
    bl_idname = "object.duplicate_object_history"
    bl_label = "Duplicate"
    bl_description = "Duplicates this history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        histories = context.scene["histories"]
        g = None
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    g = history_group
        if g is not None:
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            g.insert(g.index(obj) + 1, new_obj)
            pv_utils.replace_objects(obj, new_obj)
        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_AddNewObjectHistory(bpy.types.Operator):
    bl_idname = "object.add_new_object_history"
    bl_label = "Add A New Object History"
    bl_description = "Duplicates the current active history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "histories" in context.scene

    def execute(self, context):
        obj = context.active_object
        histories = context.scene["histories"]
        g = None
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    g = history_group
        if g is not None:
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            g.append(new_obj)
            pv_utils.replace_objects(obj, new_obj)
        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_RemoveActiveObjectHistory(bpy.types.Operator):
    bl_idname = "object.remove_active_object_history"
    bl_label = "Remove Active Object History"
    bl_description = "Removes the current active history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None or "histories" not in context.scene:
            return False
        for history_group in context.scene["histories"]:
            for item in history_group:
                if item == obj and len(history_group) == 1:
                    return False
        return True

    def execute(self, context):
        obj = context.active_object
        histories = context.scene["histories"]
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    history_group.remove(item)
                    new = history_group[-1]
                    pv_utils.replace_objects(obj, new)
        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_RemoveObjectHistory(bpy.types.Operator):
    bl_idname = "object.remove_object_history"
    bl_label = "Remove"
    bl_description = "Removes this history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        histories = context.scene["histories"]
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    history_group.remove(item)
                    if obj == context.active_object:
                        new = history_group[-1]
                        pv_utils.replace_objects(obj, new)
                    break
        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_SelectObjectHistory(bpy.types.Operator):
    bl_idname = "object.select_object_history"
    bl_label = "Select Object History"
    bl_description = "Selects this history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    new_obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "histories" in context.scene

    def execute(self, context):
        old = context.active_object
        new = bpy.data.objects[self.new_obj_name]
        pv_utils.replace_objects(old, new)
        return {'FINISHED'}


class OP_MoveObjectHistory(bpy.types.Operator):
    bl_idname = "object.move_object_history"
    bl_label = "Move Object History"
    bl_description = "Moves this history object up or down"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    dir: bpy.props.StringProperty()
    obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        dir = 1 if self.dir == "DOWN" else -1
        obj = bpy.data.objects[self.obj_name]
        histories: list = context.scene["histories"]
        group: list
        for group in histories:
            for item in group:
                if item == obj:
                    i = group.index(item)
                    group.insert(i + dir, group.pop(i))
                    break

        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_LinkObjectHistory(bpy.types.Operator):
    bl_idname = "object.link_object_history"
    bl_label = "Link Object History"
    bl_description = "Links object history of selected objects into the active object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        obj = context.active_object
        other = [x for x in context.selected_objects if x != obj]

        merge_groups = []
        histories: list = context.scene["histories"]
        for group in histories:
            for item in group:
                if (item == obj or item in other) and group not in merge_groups:
                    merge_groups.append(group)

        for group in merge_groups:
            histories.remove(group)
        final_group = list(pv_utils.flatten(merge_groups))
        for item in other:
            if item not in final_group:
                final_group.append(item)
        histories.append(final_group)

        for other_obj in other:
            other_obj.users_collection[0].objects.unlink(other_obj)

        context.scene["histories"] = histories

        return {'FINISHED'}


class OP_UnlinkObjectHistory(bpy.types.Operator):
    bl_idname = "object.unlink_object_history"
    bl_label = "Unlink Object History"
    bl_description = "Unlinks this history object out of the history"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        histories = context.scene["histories"]
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    history_group.remove(item)
                    new: bpy.types.Object = history_group[-1]
                    pv_utils.replace_objects(obj, new)
                    new.users_collection[0].objects.link(obj)
                    new.select_set(False)
                    obj.select_set(True)
                    context.view_layer.objects.active = obj

        context.scene["histories"] = histories
        return {'FINISHED'}


class OP_CopyObjectHistory(bpy.types.Operator):
    bl_idname = "object.copy_object_history"
    bl_label = "Copy"
    bl_description = "Copies/Cuts this history object"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    obj_name: bpy.props.StringProperty()
    is_cut: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene

    def execute(self, context):
        global HISTORY_COPY_OBJECT
        global HISTORY_COPY_IS_CUT
        HISTORY_COPY_OBJECT = bpy.data.objects[self.obj_name]
        HISTORY_COPY_IS_CUT = self.is_cut
        return {'FINISHED'}


class OP_PasteObjectHistory(bpy.types.Operator):
    bl_idname = "object.paste_object_history"
    bl_label = "Paste"
    bl_description = "Pastes the copied history object next to this one"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    obj_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return "histories" in context.scene and HISTORY_COPY_OBJECT is not None

    def execute(self, context):
        global HISTORY_COPY_OBJECT
        global HISTORY_COPY_IS_CUT
        obj = bpy.data.objects[self.obj_name]
        histories: list = context.scene["histories"]

        if HISTORY_COPY_IS_CUT:
            group: list
            for group in histories:
                if HISTORY_COPY_OBJECT in group:
                    group.remove(HISTORY_COPY_OBJECT)
                    if len(group) == 0:
                        histories.remove(group)
                    else:
                        HISTORY_COPY_OBJECT.users_collection[0].objects.link(group[-1])
                    HISTORY_COPY_OBJECT.users_collection[0].objects.unlink(HISTORY_COPY_OBJECT)
                    break
            for group in histories:
                if obj in group:
                    group.insert(group.index(obj) + 1, HISTORY_COPY_OBJECT)
                    break
            HISTORY_COPY_OBJECT = None
            HISTORY_COPY_IS_CUT = False
        else:
            for group in histories:
                if obj in group:
                    new_obj = HISTORY_COPY_OBJECT.copy()
                    new_obj.data = HISTORY_COPY_OBJECT.data.copy()
                    group.insert(group.index(obj) + 1, new_obj)
        context.scene["histories"] = histories
        return {'FINISHED'}


classes = [
    OP_InitializeObjectHistory,
    OP_DeleteAllObjectHistory,

    OP_AddNewObjectHistory,
    OP_RemoveActiveObjectHistory,

    OP_SelectObjectHistory,
    OP_MoveObjectHistory,

    OP_LinkObjectHistory,
    OP_UnlinkObjectHistory,

    OP_DuplicateObjectHistory,
    OP_RemoveObjectHistory,

    OP_CopyObjectHistory,
    OP_PasteObjectHistory,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
