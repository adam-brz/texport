import bpy

from .operators import (
    OBJECT_OT_ChangeExtensionForAll,
    OBJECT_OT_Export,
    OBJECT_OT_Refresh,
    OBJECT_OT_SelectAll,
)


class TextureExportPanel(bpy.types.Panel):
    bl_label = "Export Textures"
    bl_idname = "OBJECT_PT_texport_texture_export_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        options = context.scene.texport_plugin_options

        col.prop(options, "output_directory")
        col.prop(options, "global_extension")

        row = col.row()
        row.operator(OBJECT_OT_Refresh.bl_idname, text="Refresh", icon="FILE_REFRESH")
        row.operator(
            OBJECT_OT_SelectAll.bl_idname,
            text="Select/Deselect All",
            icon="SELECT_SUBTRACT",
        )
        row.operator(
            OBJECT_OT_ChangeExtensionForAll.bl_idname,
            text="Change Ext For All",
            icon="IMAGE_DATA",
        )

        col.template_list(
            "TEXPORT_UL_images",
            "",
            context.scene,
            "textures_list",
            context.scene,
            "textures_list_active_index",
        )

        col.operator(OBJECT_OT_Export.bl_idname, text="Export")
