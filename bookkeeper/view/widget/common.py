# pylint: disable=import-error,no-name-in-module

"""
Модуль общих виджетов.
"""

from typing import Callable
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QFrame, QLabel, QGridLayout,
    QAbstractItemView, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTreeView
)
from PySide6.QtGui import QStandardItemModel


class CategoryDropdown(QComboBox):
    """Дропдаун категорий."""
    def set_data(self, data: list[list[str]]) -> None:
        """Устанавливает данные для дропдауна."""
        self.clear()
        for category in data:
            self.addItem(category[1], category[0])

    def get_selected_category_id(self) -> int:
        """Отдает id (pk) категории, выбранной в дропдауне."""
        return int(self.itemData(self.currentIndex()))

    def set_current_item(self, name: str) -> None:
        """Устанавливает заданную категорию."""
        if name == '':
            name = 'None'
        self.setCurrentIndex(self.findText(name))


class EditButtons(QFrame):  # pylint: disable=too-few-public-methods
    """Кнопки контроля: добавление, обновление, удаление."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.add_btn = QPushButton('Добавить')
        layout.addWidget(self.add_btn)

        self.update_btn = QPushButton('Обновить')
        layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton('Удалить')
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(2)


class EditWindow(QWidget):  # pylint: disable=too-few-public-methods
    """Окно редактирования. Контент варьируется."""
    def __init__(
            self,
            window_name: str,
            content: QWidget,
            button_name: str,
            parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(window_name)

        layout = QVBoxLayout(self)

        layout.addWidget(content)
        self.action_button = QPushButton(button_name)
        layout.addWidget(self.action_button)

        self.setLayout(layout)

    def on_action_button_clicked(self, slot: Callable[[], None]) -> None:
        """Обработка нажатия на кнопку действия."""
        self.action_button.clicked.connect(slot)  # type: ignore[attr-defined]


class EditWindows:  # pylint: disable=too-few-public-methods
    """Класс содержащий окна добавления, обновления, удаления."""
    add: EditWindow
    update: EditWindow
    delete: EditWindow

    def __init__(
            self,
            name: str,  # В родительном падеже.
            add_content: QWidget,
            update_content: QWidget,
            delete_content: QWidget,
    ) -> None:
        self.add = EditWindow(
            window_name='Добавление ' + name,
            content=add_content,
            button_name='Добавить',
        )

        self.update = EditWindow(
            window_name='Обновление ' + name,
            content=update_content,
            button_name='Обновить',
        )

        self.delete = EditWindow(
            window_name='Удаление ' + name,
            content=delete_content,
            button_name='Удалить',
        )


class Table(QTableWidget):  # pylint: disable=too-few-public-methods
    """Виджет таблицы."""

    def __init__(
            self,
            headers: list[str],
            header_resize_modes: list[QHeaderView.ResizeMode],
            parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        header = self.horizontalHeader()
        for idx, header_resize_mode in enumerate(header_resize_modes):
            header.setSectionResizeMode(
                idx, header_resize_mode
            )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def set_data(self, data: list[list[str]]) -> None:
        """Заполняет таблицу."""
        self.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for column_idx, datum in enumerate(row):
                self.setItem(
                    row_idx, column_idx,
                    QTableWidgetItem(datum)
                )


class Tree(QTreeView):  # pylint: disable=too-few-public-methods
    """Иерархическая таблица категорий."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.item_model = QStandardItemModel()
        self.item_model.setHorizontalHeaderLabels(['Иерархия'])
        self.setModel(self.item_model)

    def set_data(self, data: list[list[str]]) -> None:
        """Устанавливает данные для древовидной структуры."""


class FrameViewWithControls(QFrame):
    """Виджет отображение, обрамленный рамкой, с таблицей."""
    edit_windows: EditWindows

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.edit_buttons = EditButtons()
        self.edit_buttons.add_btn.clicked.connect(  # type: ignore[attr-defined]
            self.on_add_button_clicked
        )
        self.edit_buttons.update_btn.clicked.connect(  # type: ignore[attr-defined]
            self.on_update_button_clicked
        )
        self.edit_buttons.delete_btn.clicked.connect(  # type: ignore[attr-defined]
            self.on_delete_button_clicked
        )

        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(2)

    def set_layout(self, name: str) -> None:
        """Устанавливает макет."""

    def on_add_button_clicked(self) -> None:
        """Обработка нажатия кнопки добавления."""

    def on_update_button_clicked(self) -> None:
        """Обработка нажатия кнопки обновления."""

    def on_delete_button_clicked(self) -> None:
        """Обработка нажатия кнопки удаления."""


class FrameTreeViewWithControls(FrameViewWithControls):
    """Виджет отображение дерева, обрамленный рамкой."""
    tree: Tree

    def set_layout(self, name: str) -> None:
        """Устанавливает макет."""
        layout = QVBoxLayout()

        layout.addWidget(QLabel(name))
        layout.addWidget(self.tree)
        layout.addWidget(self.edit_buttons)

        self.setLayout(layout)


class FrameTableViewWithControls(FrameViewWithControls):
    """Виджет отображение дерева, обрамленный рамкой."""
    table: Table

    def set_layout(self, name: str) -> None:
        """Устанавливает макет."""
        layout = QVBoxLayout()

        layout.addWidget(QLabel(name))
        layout.addWidget(self.table)
        layout.addWidget(self.edit_buttons)

        self.setLayout(layout)


class DeleteTableContent(QWidget):
    """Контент для окна редактирования таблицы."""
    row_id: int

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QGridLayout()

        self.text = QLabel()
        layout.addWidget(self.text)

        self.setLayout(layout)

    # DATA GET

    def set_row_id(self, row_id: int) -> None:
        """Устанавливает сообщение с номером заданной строки."""
        self.row_id = row_id
        self.text.setText(f'Вы точно хотите удалить строку под номером {row_id + 1}?')

    def get_row_id(self) -> int:
        """Отдает заданного номера строки."""
        return self.row_id


class AddUpdateTableContent(QWidget):   # pylint: disable=too-few-public-methods
    """Контент добавления/обновления для окна редактирования таблицы."""
    row_id: int

    def set_row(self, row_id: int, row: list[str]) -> None:
        """Устанавливает данные для контента добавления/обновления."""
