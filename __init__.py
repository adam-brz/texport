import bpy

from .operators import (
    OBJECT_OT_ChangeExtensionForAll,
    OBJECT_OT_Export,
    OBJECT_OT_Refresh,
    OBJECT_OT_SelectAll,
)

from .plugin_options import PluginOptions
from .texture_entry_properties import TextureEntryProperties
from .texture_export_panel import TextureExportPanel
from .textures_list import TEXPORT_UL_images

bl_info = {
    "name": "Texport",
    "description": "Export selected textures to any directory.",
    "blender": (3, 1, 0),
    "version": (1, 0),
    "author": "Andrew2a1",
    "support": "COMMUNITY",
    "category": "Import-Export",
    "location": "Properties > Tool > Export Textures",
}

classes = [
    TextureEntryProperties,
    PluginOptions,
    OBJECT_OT_Refresh,
    OBJECT_OT_SelectAll,
    OBJECT_OT_ChangeExtensionForAll,
    OBJECT_OT_Export,
    TEXPORT_UL_images,
    TextureExportPanel,
]

class_register, class_unregister = bpy.utils.register_classes_factory(classes)


def update_texture_list_callback():
    bpy.ops.object.texport_refresh_images()
    return 5.0


def register():
    class_register()
    bpy.types.Scene.textures_list = bpy.props.CollectionProperty(
        type=TextureEntryProperties
    )
    bpy.types.Scene.texport_plugin_options = bpy.props.PointerProperty(
        type=PluginOptions
    )
    bpy.types.Scene.textures_list_active_index = bpy.props.IntProperty(min=-1, max=-1)
    bpy.app.timers.register(update_texture_list_callback)


def unregister():
    bpy.app.timers.unregister(update_texture_list_callback)
    class_unregister()
    del bpy.types.Scene.textures_list
    del bpy.types.Scene.textures_list_active_index


if __name__ == "__main__":
    register()
