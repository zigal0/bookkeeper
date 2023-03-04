"""
Скрипт прдназначен для накатки миграций с базой данныйх SQLite.
"""

import sys
import os
import sqlite3

from enum import Enum


# CREATE_META_MIGRATION_TABLE = """CREATE TABLE IF NOT EXISTS meta_migration (
#     "id" INTEGER PRIMARY KEY AUTOINCREMENT,
#     "version_id" INTEGER UNIQUE NOT NULL,
#     "applied_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# );"""
#
# GET = """SELECT * FROM meta_migration WHERE version_id = 1;"""
#
#
# @dataclass(slots=True)
# class MetaMigration:
#     """
#     Мета информация о миграциях.
#     id - счетчик миграций
#     version_id - id маграции
#     applied_at - время применения миграции
#     """
#     id: int
#     version_id: int
#     applied_at: datetime = field(default_factory=datetime.now)


DB_FILE = 'bookkeeper.db'
AVAILABLE_MODES = ['up', 'down']
MIGRATION_DIR = "migration"


class Colors(Enum):
    """Класс с заданными константами для цветов."""
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DEFAULT = '\033[0m'


def print_fail_msg(msg: str) -> None:
    """Функция печати сообщения с FAIL."""
    print(f"{Colors.FAIL}FAIL: " + msg + f"{Colors.DEFAULT}")


def print_warning_msg(msg: str) -> None:
    """Функция печати сообщения с WARNING."""
    print(f"{Colors.WARNING}WARNING: " + msg + f"{Colors.DEFAULT}")


def print_info_msg(msg: str) -> None:
    """Функция печати сообщение с INFO."""
    print(f"{Colors.INFO}INFO: " + msg + f"{Colors.DEFAULT}")


def print_success_msg(msg: str) -> None:
    """Функция печати сообщение с SUCCESS."""
    print(f"{Colors.SUCCESS}SUCCESS: " + msg + f"{Colors.DEFAULT}")


def execute_query(query: str) -> None:
    """Выполняет запрос в базу данных"""
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(query)

    con.close()


def split_sql_queries(sql_queries: str) -> list[str]:
    """Разделяет sql запросы из файла."""
    return [query.strip() for query in sql_queries.split(';')]


def execute_migration_file(file_name: str, mode: str) -> None:
    """Запускате исполнения одного файла миграции."""
    file_name_parts = file_name.split('_')

    try:
        version_id = int(file_name_parts[0])
    except ValueError:
        print_fail_msg('Incorrect migration name')

        sys.exit()

    path = MIGRATION_DIR + "/" + file_name
    with open(path, mode='r', encoding="utf-8") as file:
        sql_script = file.read()

    up_down_scripts = sql_script.split('-- down')

    if mode == 'up':
        queries = split_sql_queries(up_down_scripts[0])
    else:
        queries = split_sql_queries(up_down_scripts[1])

    for query in queries:
        execute_query(query)

    print_info_msg(f"Migration with id = {version_id} was applied with mode {mode}")


def run_migration() -> None:
    """Основной скрипт, запускающий процесс накатки миграций."""
    if len(sys.argv) != 2:
        print_fail_msg("You need to provide one of next options: " + str(AVAILABLE_MODES))
        sys.exit()

    mode = sys.argv[1]

    if mode not in AVAILABLE_MODES:
        print_fail_msg("Mode " + mode + " is incorrect")
        sys.exit()

    all_file_names = os.listdir(MIGRATION_DIR)
    migrations = sorted([file_name for file_name in all_file_names
                         if file_name.endswith(".sql")])

    for migration_name in migrations:
        execute_migration_file(migration_name, mode)

    print_success_msg("All migration were applied")


run_migration()
