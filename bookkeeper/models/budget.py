"""
Модель бюджета
"""

from dataclasses import dataclass

ALLOWED_PERIODS = ['День', 'Неделя', 'Месяц', 'Год']


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    amount - сумма
    period - промежуток времени, на который планируется бюджет
    pk - id записи в базе данных
    """
    amount: float = 0.0
    period: str = 'День'
    pk: int = 0
