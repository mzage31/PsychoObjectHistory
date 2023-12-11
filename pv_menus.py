import bpy
from .pv_operators import (OP_DuplicateObjectHistory,
                           OP_RemoveObjectHistory,
                           OP_CopyObjectHistory,
                           OP_PasteObjectHistory,
                           OP_LinkObjectHistory,
                           OP_UnlinkObjectHistory,
                           )


class MT_HistoryObjectOptions(bpy.types.Menu):
    bl_label = ""
    bl_idname = "object_MT_history_object_options"

    obj_name = None

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text=f"Options for {self.obj_name}")
        layout.separator()

        copy = layout.operator(OP_CopyObjectHistory.bl_idname, icon="COPYDOWN")
        copy.obj_name = self.obj_name
        copy.is_cut = False
        copy = layout.operator(OP_CopyObjectHistory.bl_idname, text="Cut", icon="COPYDOWN")
        copy.obj_name = self.obj_name
        copy.is_cut = True
        layout.operator(OP_PasteObjectHistory.bl_idname, icon="PASTEDOWN").obj_name = self.obj_name
        layout.separator()
        
        layout.operator(OP_DuplicateObjectHistory.bl_idname, icon="DUPLICATE").obj_name = self.obj_name
        layout.operator(OP_RemoveObjectHistory.bl_idname, icon="TRASH").obj_name = self.obj_name
        layout.separator()
        
        layout.operator(OP_UnlinkObjectHistory.bl_idname, text="UnLink", icon='UNLINKED').obj_name = self.obj_name


class OP_MenuCaller_HistoryObjectOptions(bpy.types.Operator):
    bl_idname = "object.history_object_options_menu_caller"
    bl_label = ""

    obj_name: bpy.props.StringProperty()

    def execute(self, context):
        MT_HistoryObjectOptions.obj_name = self.obj_name
        bpy.ops.wm.call_menu('INVOKE_DEFAULT', name=MT_HistoryObjectOptions.bl_idname)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MT_HistoryObjectOptions)
    bpy.utils.register_class(OP_MenuCaller_HistoryObjectOptions)


def unregister():
    bpy.utils.unregister_class(MT_HistoryObjectOptions)
    bpy.utils.unregister_class(OP_MenuCaller_HistoryObjectOptions)
