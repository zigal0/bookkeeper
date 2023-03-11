# pylint: disable=import-error,no-name-in-module

"""
Модуль отображения основного окна приложения.
"""

from PySide6.QtWidgets import (
    QWidget, QGridLayout
)
from PySide6.QtWidgets import QMainWindow
from bookkeeper.view.widget.views.category_view import CategoryView
from bookkeeper.view.widget.views.expense_view import ExpenseView
from bookkeeper.view.widget.views.budget_view import BudgetView


class MainWindow(QMainWindow):  # pylint: disable=too-few-public-methods
    """Основное окно приложения."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(1200, 700)

        layout = QGridLayout()

        self.expense_view = ExpenseView(self)
        layout.addWidget(self.expense_view, 0, 0, 2, 1)

        self.budget_view = BudgetView(self)
        layout.addWidget(self.budget_view, 0, 1)

        self.category_view = CategoryView(self)
        layout.addWidget(self.category_view, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setColumnMinimumWidth(1, 400)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
