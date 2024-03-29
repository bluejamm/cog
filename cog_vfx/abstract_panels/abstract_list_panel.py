import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..utils import file_utils, fonts, interface_utils, quick_dialog


class AbstractListPanel(QWidget):
    def __init__(
        self,
        page_controller,
        tree_widget=None,
        info_widget=None,
        parent=None,
        object_type="object",
    ):
        super().__init__(parent)
        # assign argument variables
        self.page_controller = page_controller
        self.object_type = object_type
        self.tree_widget = tree_widget
        self.info_widget = info_widget
        self.elements = []
        # self.element_data = {}
        self.fonts = fonts.get_fonts()

        # create ui
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        # self.setMaximumWidth(self.minimumSizeHint().width())
        self.setMinimumWidth(215)
        self.setMaximumWidth(280)
        print(" MAXIMUM SIZE:", self.minimumSizeHint().width())

        # Label
        self.element_page_label = QLabel(self.object_type.title() + "s")
        self.element_page_label.setFont(self.fonts["header"])
        self.layout.addWidget(self.element_page_label)

        # Search Bar
        self.element_search_bar = QLineEdit()
        # self.element_search_bar.setMaximumWidth(self.element_search_bar.minimumSizeHint().width())
        self.element_search_bar.setTextMargins(5, 3, 5, 3)
        self.element_search_bar.setStyleSheet("QLineEdit {border-radius: 10px;}")
        search_bar_font = QFont()
        search_bar_font.setPointSize(10)
        self.element_search_bar.setFont(search_bar_font)
        self.element_search_bar.textChanged.connect(self.on_search_changed)
        self.element_search_bar.setPlaceholderText("Search...")
        self.layout.addWidget(self.element_search_bar)
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.layout.addItem(spacer)

        self.element_list = QListWidget()
        self.element_list.setSortingEnabled(True)
        self.element_list.itemSelectionChanged.connect(
            self.on_element_selection_changed
        )
        self.element_list.setAlternatingRowColors(True)
        self.element_list.setIconSize(QSize(500, 50))
        self.populate_element_list()
        self.layout.addWidget(self.element_list)
        # context menu
        self.context_menu = QMenu()
        style_sheet = interface_utils.get_style_sheet()
        self.context_menu.setStyleSheet(style_sheet)
        self.element_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.element_list.customContextMenuRequested.connect(
            lambda pos: self.context_menu.exec(self.element_list.mapToGlobal(pos))
        )

        # buttons
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addStretch()

        self.element_refresh_button = QPushButton("Refresh")
        self.element_refresh_button.clicked.connect(self.populate_element_list)
        bottom_buttons_layout.addWidget(self.element_refresh_button)

        self.new_element_button = QPushButton("+")
        self.new_element_button.setMaximumWidth(25)
        self.new_element_button.clicked.connect(self.on_element_add)
        bottom_buttons_layout.addWidget(self.new_element_button)

        self.delete_element_button = QPushButton("-")
        self.delete_element_button.setMaximumWidth(25)
        self.delete_element_button.clicked.connect(self.on_element_delete)
        bottom_buttons_layout.addWidget(self.delete_element_button)

        self.layout.addLayout(bottom_buttons_layout)

    def on_search_changed(self, search_text):
        for element_index in range(self.element_list.count()):
            element_item = self.element_list.item(element_index)
            if not search_text.lower() in element_item.text().lower():
                element_item.setHidden(True)
            else:
                element_item.setHidden(False)

    def on_element_selection_changed(self):
        if self.page_controller:
            selected_items = self.element_list.selectedItems()
            if len(selected_items) > 0:
                selected_objects = []
                for selected_item in selected_items:
                    selected_object = interface_utils.get_list_widget_data(
                        item=selected_item
                    )
                    selected_objects.append(selected_object)
                self.page_controller.change_element_selection(selected_objects)
        # if self.info_widget:
        #     self.info_widget.update_panel_info(self.element_list)
        # if self.tree_widget:
        #     self.tree_widget.populate_file_tree()

    def update_element_info(self):
        pass

    def populate_element_list(self, directory=None):
        # check for previous selection
        prev_selected_items = self.element_list.selectedItems()
        has_prev_selection = len(prev_selected_items) != 0
        prev_selected_object = None
        if has_prev_selection:
            prev_selected_object = interface_utils.get_list_widget_data(
                item=prev_selected_items[0]
            )

        self.element_list.clear()
        elements = self.page_controller.elements

        new_items = []
        for element_data in elements:
            item_label = (
                element_data.element_type.title() + " " + element_data.formatted_name
            )
            item = QListWidgetItem(item_label, self.element_list)

            interface_utils.set_list_widget_data(item, element_data)
            item.setIcon(element_data.thumbnail)

            if has_prev_selection and element_data is prev_selected_object:
                item.setSelected(True)

        if not has_prev_selection:
            self.element_list.item(0).setSelected(True)
        return new_items

    def update_all_thumbnails(self):
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            self.update_thumbnail(item)

    def update_thumbnail(self, item):
        element_data = interface_utils.get_list_widget_data(item=item)
        if not element_data:
            print("thumbnail could not be updated")
            return False
        thumbnail_path = os.path.join(element_data["dir"], "thumbnail.png")
        item.setIcon(QIcon(thumbnail_path))
        return True

    def get_elements(self, element_name_filter):
        print("get_elements method meant to be overloaded")
        return {}

    def set_elements(self):
        print("set_elements method meant to be overloaded")

    def on_element_add(self):
        print("on_element_add method meant to be overloaded")

    def on_element_delete(self):
        print("element delete")
        quick_dialog(self, "Deleting elements isn't implemented yet")


class NewObjectInterface(QDialog):
    def __init__(self, parent=None, element_list=None, edit=False, element_data=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("New Object")
        self.resize(400, 600)
        self.element_list = element_list

        # edit mode stuff
        self.edit_mode = edit
        self.existing_element_data = element_data

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_bottom_buttons():
        # bottom buttons
        bottom_buttons_layout = QHBoxLayout()
        bottom_button_min_size = (50, 30)
        ok_button = QPushButton("ok")
        cancel_button = QPushButton("cancel")
        ok_button.clicked.connect(self.on_ok_pressed)
        cancel_button.clicked.connect(self.on_cancel_pressed)
        ok_button.setMinimumSize(*bottom_button_min_size)
        cancel_button.setMinimumSize(*bottom_button_min_size)
        bottom_buttons_layout.addStretch()
        # add widgets
        bottom_buttons_layout.addWidget(ok_button)
        bottom_buttons_layout.addWidget(cancel_button)
        self.layout.addLayout(bottom_buttons_layout)

    def on_element_add(self):
        print("on_element_add method meant to be overriden")

    def on_element_edit(self):
        print("on_element_edit method meant to be overriden")
