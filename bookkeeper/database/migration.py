import sys
import os
import sqlite3

# TODO: Требуется мета таблица, для слежки за миграциями.
# from dataclasses import dataclass, field
# from datetime import datetime
#
#
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


DB_FILE = '../repository/bookkeeper.db'
AVAILABLE_MODES = ['up', 'down']
MIGRATION_DIR = "migration"


class Colors:
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DEFAULT = '\033[0m'


def print_fail_msg(msg: str) -> None:
    print(f"{Colors.FAIL}FAIL: " + msg + f"{Colors.DEFAULT}")


def print_warning_msg(msg: str) -> None:
    print(f"{Colors.WARNING}WARNING: " + msg + f"{Colors.DEFAULT}")


def print_info_msg(msg: str) -> None:
    print(f"{Colors.INFO}INFO: " + msg + f"{Colors.DEFAULT}")


def print_success_msg(msg: str) -> None:
    print(f"{Colors.SUCCESS}SUCCESS: " + msg + f"{Colors.DEFAULT}")


def execute_query(query: str) -> None:
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(query)

    con.close()


def split_sql_queries(sql_queries: str) -> list[str]:
    return [query.strip() for query in sql_queries.split(';')]


# run_migration runs 1 file of migrations
def run_migration(file_name: str) -> None:
    file_name_parts = file_name.split('_')

    try:
        version_id = int(file_name_parts[0])
    except ValueError:
        print_fail_msg('Incorrect migration name')

        sys.exit()

    path = MIGRATION_DIR + "/" + file_name
    with open(path, mode='r') as file:
        sql_script = file.read()

    up_down_scripts = sql_script.split('-- down')

    if mode == 'up':
        queries = split_sql_queries(up_down_scripts[0])
    else:
        queries = split_sql_queries(up_down_scripts[1])

    for query in queries:
        execute_query(query)

    print_info_msg(f"Migration with id = {version_id} was applied with mode {mode}")


# main script
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
    run_migration(migration_name)

print_success_msg("All migration were applied")

# Try to create fast schemas

