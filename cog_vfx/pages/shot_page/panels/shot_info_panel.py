from ....abstract_panels.abstract_info_panel import AbstractInfoPanel
from ....utils.file_utils import get_pkg_asset_path


# create side panel for showing shot information
class ShotInfoPanel(AbstractInfoPanel):
    def __init__(self, shot_controller, parent=None):
        super().__init__(shot_controller, parent)
        self.shot_controller = shot_controller

        # title
        self.title.setText("Shot Info")

        self.update_data = [
            "start_frame",
            "end_frame",
            "fps",
            "shot_num",
            "description",
            "res_width",
            "res_height",
        ]
        self.update_data_mapping = None

        # create sections
        self.create_sections()
        self.create_bottom_buttons()

    # def on_object_edit(self):
    #     asset_list =
    #     self.edit_asset_window = NewAssetInterface(self, shot_list, edit=True, asset_data=selected_asset_data)
    #     self.edit_asset_window.exec()

    def create_sections(self):
        # thumbnail
        thumbnail_dir = get_pkg_asset_path("assets/icons/missing_shot_thumbnail.png")
        _, self.shot_thumbnail = self.new_thumbnail(thumbnail_dir)

        # render data section
        self.render_data_section = self.new_section("Render Data")
        self.shot_num = self.render_data_section.add_label("SH: {shot_num}")
        self.frame_range = self.render_data_section.add_label(
            "Frame Range: {start_frame} - {end_frame}"
        )
        self.render_res = self.render_data_section.add_label(
            "Resolution: {res_width} x {res_height}"
        )
        self.render_fps = self.render_data_section.add_label("FPS: {fps}")
        self.render_fps = self.render_data_section.add_label("test: {test}")

        # description section
        self.description_section = self.new_section("Description")
        self.description_label = self.description_section.add_label("{description}")
        # self.update_sections({"{shot_num}":"hello"})

    def update_panel_info(self):
        selected_element = self.shot_controller.get_selected_element()
        if not selected_element:
            return
        super().update_panel_info()
        self.shot_thumbnail.set_image(selected_element.thumbnail_path)
