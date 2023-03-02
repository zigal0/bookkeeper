"""
Описан класс, представляющий бюджет
"""

from dataclasses import dataclass
from enum import Enum


class Period(Enum):
    DAY = 1
    WEEK = 2
    MONTH = 3


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    amount - сумма
    category - id категории бюджета
    period - промежуток времени, на который планируется бюджет
    """
    amount: int
    category: int
    period: Period
    pk: int = 0

