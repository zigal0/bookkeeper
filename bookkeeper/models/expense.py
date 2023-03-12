"""
Модель расхода
"""

from dataclasses import dataclass
from datetime import datetime, date

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    pk - id записи в базе данных
    amount - сумма
    category_id - id категории расходов
    comment - комментарий
    expense_date - дата расхода
    added_date - дата добавления в бд
    """
    amount: float = 0.0
    category_id: int | None = None
    comment: str = ''
    expense_date: date = date.today()
    added_date: datetime = datetime.now().replace(microsecond=0)
    pk: int = 0
