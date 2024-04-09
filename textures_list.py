import bpy


class TEXPORT_UL_images(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        icon = self._load_icon(item.texture_name)
        row = layout.row(align=True)
        if self.layout_type in {"DEFAULT", "COMPACT", "GRID"}:
            row.prop(item, "export", text="")
            if icon:
                row.template_icon(icon)
            tex_name_row = row.row()
            tex_name_row.scale_x = 2
            tex_name_row.prop(item, "texture_name", text="", emboss=False)
            row.prop(item, "output_format", text="")

    def filter_items(self, context, data, propname):
        texture_properties = getattr(data, propname)

        flt_flags = []
        flt_neworder = []

        if self.filter_name:
            flt_flags = bpy.types.UI_UL_list.filter_items_by_name(
                self.filter_name,
                self.bitflag_filter_item,
                texture_properties,
                "texture_name",
                reverse=self.use_filter_invert,
            )
            if self.use_filter_invert:
                flt_flags = list(map(lambda x: x ^ self.bitflag_filter_item, flt_flags))

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(texture_properties)

        if self.use_filter_sort_alpha:
            flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(
                texture_properties, "texture_name"
            )

        return flt_flags, flt_neworder

    def _load_icon(self, texture_name):
        try:
            return bpy.types.UILayout.icon(bpy.data.images[texture_name])
        except:
            return None
