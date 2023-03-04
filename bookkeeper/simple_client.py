"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

DB_FILE = 'database/bookkeeper.db'

category_repository = SQLiteRepository[Category](DB_FILE, Category)
expense_repository = SQLiteRepository[Expense](DB_FILE, Expense)
budget_repository = SQLiteRepository[Budget](DB_FILE, Budget)


cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), category_repository)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*category_repository.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*expense_repository.get_all(), sep='\n')
    # elif cmd == 'бюджет':
    #     print(*budget_repository.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = category_repository.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        expense_repository.add(exp)
        print(exp)
