import bpy
from .pv_operators import (OP_InitializeObjectHistory,
                           OP_DeleteAllObjectHistory,
                           OP_AddNewObjectHistory,
                           OP_RemoveActiveObjectHistory,
                           OP_SelectObjectHistory,
                           OP_LinkObjectHistory,
                           OP_MoveObjectHistory)
from .pv_menus import OP_MenuCaller_HistoryObjectOptions


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
            layout.operator(OP_InitializeObjectHistory.bl_idname, icon='FILE_REFRESH')
            return

        histories = context.scene["histories"]
        my_group = None
        for history_group in histories:
            for item in history_group:
                if item == obj:
                    my_group = history_group

        if my_group is None:
            layout.operator(OP_InitializeObjectHistory.bl_idname, icon='FILE_REFRESH')
            return

        row = layout.row()
        col = row.column()

        for item in my_group:
            item_row = col.row(align=True)
            item_row.scale_y = 2
            item_row.label(text="", icon="OBJECT_DATA")
            item_row.prop(item, "name", text="")
            inner_col = item_row.column(align=True)
            inner_col.scale_x = 1.3
            inner_col.operator(OP_SelectObjectHistory.bl_idname, text="", depress=item == obj, icon="RESTRICT_VIEW_OFF" if item == obj else "RESTRICT_VIEW_ON").new_obj_name = item.name

            inner_col = item_row.column(align=True)
            inner_col.scale_y = 0.5 
            move = inner_col.operator(OP_MoveObjectHistory.bl_idname, text="", icon="TRIA_UP")
            move.dir = 'UP'
            move.obj_name = item.name
            move = inner_col.operator(OP_MoveObjectHistory.bl_idname, text="", icon="TRIA_DOWN")
            move.dir = 'DOWN'
            move.obj_name = item.name
            item_row.operator(OP_MenuCaller_HistoryObjectOptions.bl_idname, text="", icon="DOWNARROW_HLT").obj_name = item.name

        side = row.column()
        col = side.column(align=True)
        col.operator(OP_AddNewObjectHistory.bl_idname, icon='ADD', text="")
        if len(my_group) == 1:
            col.operator(OP_DeleteAllObjectHistory.bl_idname, icon='REMOVE', text="")
        else:
            col.operator(OP_RemoveActiveObjectHistory.bl_idname, icon='REMOVE', text="")

        col = side.column(align=True)
        col.operator(OP_LinkObjectHistory.bl_idname, icon='LINKED', text="")

        col = side.column(align=True)
        col.operator(OP_DeleteAllObjectHistory.bl_idname, icon='TRASH', text="")


def register():
    bpy.utils.register_class(ObjectHistoryPanel)


def unregister():
    bpy.utils.unregister_class(ObjectHistoryPanel)
