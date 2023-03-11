# pylint: disable=import-error,no-name-in-module

"""
Модуль отображения бюджета.
"""

from typing import Tuple
from PySide6.QtWidgets import (
    QLabel, QWidget, QHeaderView,
    QComboBox, QGridLayout, QDoubleSpinBox
)
from bookkeeper.models.budget import ALLOWED_PERIODS, Budget
from bookkeeper.view.widget.common import (
    DeleteTableContent, Table, FrameTableViewWithControls,
    EditWindows, AddUpdateTableContent
)

HEADERS = ["Период", "Сумма", "Бюджет"]


class BudgetView(FrameTableViewWithControls):
    """Отображение бюджета."""
    budgets: list[list[str]]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        header_resize_modes = [
            QHeaderView.ResizeMode.ResizeToContents,
            QHeaderView.ResizeMode.Stretch,
            QHeaderView.ResizeMode.Stretch
        ]

        self.table = Table(HEADERS, header_resize_modes, self)
        self.set_layout('Бюджет')

        self.add_content = AddUpdateContent()
        self.update_content = AddUpdateContent()
        self.delete_content = DeleteTableContent()

        self.edit_windows = EditWindows(
            'бюджета',
            self.add_content,
            self.update_content,
            self.delete_content
        )

        self.edit_windows.add.setFixedSize(300, 150)
        self.edit_windows.update.setFixedSize(300, 150)
        self.edit_windows.delete.setFixedSize(400, 100)

    def set_up(self, budgets: list[list[str]]) -> None:
        """Устанавливает данные для виджета."""
        self.budgets = budgets
        self.table.set_data(budgets)

    # Actions

    def on_add_button_clicked(self) -> None:
        """Обработка нажатия кнопки добавления."""
        self.edit_windows.add.show()

    def on_update_button_clicked(self) -> None:
        """Обработка нажатия кнопки обновления."""
        row_id = self.table.currentRow()
        if row_id < 0:
            return

        self.update_content.set_row(row_id, self.budgets[self.table.currentRow()])
        self.edit_windows.update.show()

    def on_delete_button_clicked(self) -> None:
        """Обработка нажатия кнопки удаления."""
        row_id = self.table.currentRow()
        if row_id < 0:
            return

        self.delete_content.set_row_id(row_id)
        self.edit_windows.delete.show()


class AddUpdateContent(AddUpdateTableContent):
    """Контент добавления/обновления для окна редактирования бюджета."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QGridLayout(self)

        layout.addWidget(QLabel('Период'), 1, 0)
        self.period_dropdown = QComboBox()
        for period in ALLOWED_PERIODS:
            self.period_dropdown.addItem(period)
        layout.addWidget(self.period_dropdown, 1, 1)

        layout.addWidget(QLabel('Бюджет'), 2, 0)
        self.amount = QDoubleSpinBox()
        self.amount.setMinimum(0)
        self.amount.setMaximum(100000)
        layout.addWidget(self.amount, 2, 1)

        self.setLayout(layout)

    # DATA GET

    def get_period(self) -> str:
        """Получение периода бюджета."""
        return self.period_dropdown.currentText()

    def get_amount(self) -> float:
        """Получение бюджета на период."""
        return float(self.amount.value())

    def get_budget_update(self) -> Tuple[int, Budget]:
        """Получение бюджета для обновления."""
        return self.row_id, self.get_budget_add()

    def get_budget_add(self) -> Budget:
        """Получение бюджета для добавления."""
        return Budget(
            amount=self.get_amount(),
            period=self.get_period(),
        )

    # DATA SET

    def set_row(self, row_id: int, row: list[str]) -> None:
        """Устанавливает данные для окно редактирования."""
        self.row_id = row_id
        self.amount.setValue(float(row[2]))
        self.period_dropdown.setCurrentIndex(self.period_dropdown.findText(row[0]))
