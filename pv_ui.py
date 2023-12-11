import bpy
from .pv_operators import (OP_InitObjectHistory,
                           OP_DeleteObjectHistory,
                           OP_AddObjectHistory,
                           OP_RemoveObjectHistory,
                           OP_SelectObjectHistory,
                           OP_LinkObjectHistory,
                           OP_UnlinkObjectHistory)


class ObjectHistoryPanel(bpy.types.Panel):
    bl_label = "Psycho History"
    bl_idname = "DATA_PT_PsychoHistory"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_category = " "

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        obj = context.active_object
        layout = self.layout

        if "histories" not in context.scene:
            layout.operator(OP_InitObjectHistory.bl_idname, icon='FILE_REFRESH')
            return

        histories = context.scene["histories"]
        my_group = None
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    my_group = history_group

        if my_group is None:
            layout.operator(OP_InitObjectHistory.bl_idname, icon='FILE_REFRESH')
            return

        row = layout.row()
        col = row.column(align=True)

        for item in my_group:
            item_row = col.row(align=True)
            item_row.label(text="", icon="OBJECT_DATA")
            item_row.prop(item, "name", text="")
            item_row.operator(OP_SelectObjectHistory.bl_idname, text="", depress=item == obj, icon="RESTRICT_VIEW_OFF" if item == obj else "RESTRICT_VIEW_ON").new_obj_name = item.name

        side = row.column()
        col = side.column(align=True)
        col.operator(OP_AddObjectHistory.bl_idname, icon='ADD', text="")
        if len(my_group) == 1:
            col.operator(OP_DeleteObjectHistory.bl_idname, icon='REMOVE', text="")
        else:
            col.operator(OP_RemoveObjectHistory.bl_idname, icon='REMOVE', text="")

        col = side.column(align=True)
        col.operator(OP_LinkObjectHistory.bl_idname, icon='LINKED', text="")
        col.operator(OP_UnlinkObjectHistory.bl_idname, icon='UNLINKED', text="")

        col = side.column(align=True)
        col.operator(OP_DeleteObjectHistory.bl_idname, icon='TRASH', text="")

    
def register():
    bpy.utils.register_class(ObjectHistoryPanel)


def unregister():
    bpy.utils.unregister_class(ObjectHistoryPanel)
