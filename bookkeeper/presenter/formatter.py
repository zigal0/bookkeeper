"""
Модуль содержит функцию форматирования данных в требуемый формат для view.
"""

from datetime import date, timedelta
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


def format_expense_data(
        expenses: list[Expense],
        category_id_to_name: dict[int, str]
) -> list[list[str]]:
    """Форматирует данные о расходах"""
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
    """Форматирует данные о категориях"""
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


def format_budget_data(budgets: list[Budget], expenses: list[Expense]) -> list[list[str]]:
    """Форматирует данные о бюджете"""
    res = []
    current_date = date.today()
    start_date = current_date
    finish_date = current_date
    for budget in budgets:
        if budget.period == 'День':
            start_date = current_date
            finish_date = start_date + timedelta(days=1)
        elif budget.period == 'Неделя':
            start_date = current_date - timedelta(days=current_date.weekday())
            finish_date = start_date + timedelta(weeks=1)
        elif budget.period == 'Месяц':
            start_date = current_date.replace(day=1)
            finish_date = \
                start_date.replace(month=current_date.month + 1) - timedelta(days=1)
        elif budget.period == 'Год':
            start_date = current_date.replace(day=1, month=1)
            finish_date = start_date.replace(year=current_date.year + 1)

        general_expense = calculate_expenses_in_period(
            expenses,
            start_date,
            finish_date
        )
        res.append([
            str(budget.period),
            str(budget.amount),
            str(general_expense),
        ])

    return res


def calculate_expenses_in_period(
        expenses: list[Expense],
        start_date: date,
        finish_date: date
) -> float:
    """
    Функция подсчитывает суммарные траты за заданный промежуток:
    start_date - включительно, finish_date - исключая.
    """
    general_expense = 0.0
    for expense in expenses:
        if start_date <= expense.expense_date < finish_date:
            general_expense += expense.amount

    return round(general_expense, 2)
