"""
Модуль содержит функцию форматирования данных в требуемый формат для view.
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


def format_expense_data(
        expenses: list[Expense],
        category_id_to_name: dict[int, str]
) -> list[list[str]]:
    res = []
    for expense in expenses:
        category = ''
        if expense.category_id is not None \
                and expense.category_id in category_id_to_name:
            category = category_id_to_name[expense.category_id]

        res.append([
            str(expense.expense_date),
            str(expense.amount),
            category,
            expense.comment,
        ])

    return res


def format_category_data(categories: list[Category]) -> list[list[str]]:
    res = [[str(0), '', str(0)]]
    for category in categories:
        parent_id = 0
        if category.parent_id is not None:
            parent_id = category.parent_id
        res.append([
            str(category.pk),
            str(category.name),
            str(parent_id),
        ])

    return res


def format_budget_data(budgets: list[Budget]) -> list[list[str]]:
    res = []
    for budget in budgets:
        res.append([
            str(budget.period),
            str(0),
            str(budget.amount),
        ])

    return res
