# pylint: disable=import-error,no-name-in-module

"""
Файл для запуска приложения.
"""

import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.view.main_window import MainWindow
from bookkeeper.presenter.presenter import Presenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository

DB_NAME = 'database/bookkeeper.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()
    view.show()

    category_repository = SQLiteRepository[Category](DB_NAME, Category)
    expense_repository = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repository = SQLiteRepository[Budget](DB_NAME, Budget)

    window = Presenter(
        view,
        category_repository,
        expense_repository,
        budget_repository,
    )
    window.show()

    sys.exit(app.exec())
