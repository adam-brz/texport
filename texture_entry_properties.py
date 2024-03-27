import bpy


class TextureEntryProperties(bpy.types.PropertyGroup):
    texture_name: bpy.props.StringProperty(
        name="Texture name",
        description="Name of the texture",
    )
    export: bpy.props.BoolProperty(
        name="Export",
        description="Value indicating if this texture should be exported",
        default=False,
    )
    output_format: bpy.props.StringProperty(
        name="Output format",
        description="Output format for texture (see supported images: https://docs.blender.org/manual/en/latest/files/media/image_formats.html)",
        default="jpg",
    )
