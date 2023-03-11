"""
Модуль содержит в себе основую бизнес логику приложения.
"""

from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.presenter import formatter
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.view.main_window import MainWindow


class Presenter:
    categories: list[Category]
    expenses: list[Expense]
    budgets: list[Budget]
    category_id_to_name: dict[int, str] = {}

    def __init__(
            self,
            view: MainWindow,
            category_repository: SQLiteRepository[Category],
            expense_repository: SQLiteRepository[Expense],
            budget_repository: SQLiteRepository[Budget],
    ) -> None:
        self.view = view

        self.category_repository = category_repository
        self.expense_repository = expense_repository
        self.budget_repository = budget_repository

        self.get_data()

        # Add handlers

        self.view.category_view.edit_windows.add. \
            on_action_button_clicked(self.handle_add_category_clicked)
        self.view.category_view.edit_windows.update. \
            on_action_button_clicked(self.handle_update_category_clicked)
        self.view.category_view.edit_windows.delete. \
            on_action_button_clicked(self.handle_delete_category_clicked)

        self.view.expense_view.edit_windows.add. \
            on_action_button_clicked(self.handle_add_expense_clicked)
        self.view.expense_view.edit_windows.update. \
            on_action_button_clicked(self.handle_update_expense_clicked)
        self.view.expense_view.edit_windows.delete. \
            on_action_button_clicked(self.handle_delete_expense_clicked)

        self.view.budget_view.edit_windows.add. \
            on_action_button_clicked(self.handle_add_budget_clicked)
        self.view.budget_view.edit_windows.update. \
            on_action_button_clicked(self.handle_update_budget_clicked)
        self.view.budget_view.edit_windows.delete. \
            on_action_button_clicked(self.handle_delete_budget_clicked)

    def get_categories(self) -> None:
        self.categories = self.category_repository.get_all()
        self.category_id_to_name.clear()
        for category in self.categories:
            self.category_id_to_name[category.pk] = category.name

    def get_data(self) -> None:
        self.get_categories()
        self.budgets = self.budget_repository.get_all()
        self.expenses = self.expense_repository.get_all()

    def show(self) -> None:
        self.view.category_view.set_up(
            formatter.format_category_data(self.categories)
        )
        self.view.expense_view.set_up(
            formatter.format_expense_data(self.expenses, self.category_id_to_name),
            formatter.format_category_data(self.categories)
        )
        self.view.budget_view.set_up(
            formatter.format_budget_data(self.budgets)
        )
        self.view.show()

    # ON UPDATES

    def on_categories_updated(self) -> None:
        self.get_categories()
        self.view.category_view.set_up(
            formatter.format_category_data(self.categories)
        )
        self.view.expense_view.set_up(
            formatter.format_expense_data(self.expenses, self.category_id_to_name),
            formatter.format_category_data(self.categories)
        )

    def on_expenses_updated(self) -> None:
        self.expenses = self.expense_repository.get_all()
        self.view.expense_view.set_up(
            formatter.format_expense_data(self.expenses, self.category_id_to_name),
            formatter.format_category_data(self.categories)
        )
        self.view.budget_view.set_up(
            formatter.format_budget_data(self.budgets)
        )

    def on_budgets_updated(self) -> None:
        self.budgets = self.budget_repository.get_all()
        self.view.budget_view.set_up(
            formatter.format_budget_data(self.budgets)
        )

    # CATEGORY HANDLERS

    def handle_add_category_clicked(self) -> None:
        category = self.view.category_view.add_content.get_category_add()
        if category.name in ['None', '']:
            return

        if category.parent_id == 0:
            category.parent_id = None

        self.category_repository.add(category)
        self.view.category_view.edit_windows.add.hide()
        self.on_categories_updated()

    def handle_update_category_clicked(self) -> None:
        category = self.view.category_view.update_content.get_category_update()
        if category.name in ['None', '']:
            return

        if category.parent_id == 0:
            category.parent_id = None

        self.category_repository.update(category)
        self.view.category_view.edit_windows.update.hide()
        self.on_categories_updated()

    def handle_delete_category_clicked(self) -> None:
        pk_to_delete = self.view.category_view.delete_content.get_category_pk_to_delete()
        if pk_to_delete == 0:
            return

        self.category_repository.delete(pk_to_delete)
        self.view.category_view.edit_windows.delete.hide()
        self.on_categories_updated()

    # EXPENSE HANDLERS

    def handle_add_expense_clicked(self) -> None:
        expense = self.view.expense_view.add_content.get_expense_add()
        if expense.category_id == 0:
            expense.category_id = None

        self.expense_repository.add(expense)
        self.view.expense_view.edit_windows.add.hide()
        self.on_expenses_updated()

    def handle_update_expense_clicked(self) -> None:
        row_id, expense = self.view.expense_view.update_content.get_expense_update()
        if expense.category_id == 0:
            expense.category_id = None
        expense.pk = self.expenses[row_id].pk

        self.expense_repository.update(expense)
        self.view.expense_view.edit_windows.update.hide()
        self.on_expenses_updated()

    def handle_delete_expense_clicked(self) -> None:
        row_id = self.view.expense_view.delete_content.get_row_id()
        self.expense_repository.delete(self.expenses[row_id].pk)
        self.view.expense_view.edit_windows.delete.hide()
        self.on_expenses_updated()

    # BUDGET HANDLERS

    def handle_add_budget_clicked(self) -> None:
        budget = self.view.budget_view.add_content.get_budget_add()
        self.budget_repository.add(budget)
        self.view.budget_view.edit_windows.add.hide()
        self.on_budgets_updated()

    def handle_update_budget_clicked(self) -> None:
        row_id, budget = self.view.budget_view.update_content.get_budget_update()
        budget.pk = self.budgets[row_id].pk
        self.budget_repository.update(budget)
        self.view.budget_view.edit_windows.update.hide()
        self.on_budgets_updated()

    def handle_delete_budget_clicked(self) -> None:
        row_id = self.view.budget_view.delete_content.get_row_id()
        pk = self.budgets[row_id].pk
        self.budget_repository.delete(pk)
        self.view.budget_view.edit_windows.delete.hide()
        self.on_budgets_updated()
