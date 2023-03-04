"""
Модуль описывает репозиторий, работающий с СУБД SQLite.
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from datetime import datetime


from bookkeeper.repository.abstract_repository import AbstractRepository, T

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class SQLiteRepository(AbstractRepository[T]):
    """
    Основной репозиторий для работы с СУБД SQLite.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls

        # queries help
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        fields_update = ", ".join([f"{field}=?" for field in self.fields.keys()])

        self.queries = {
            'foreign_keys': 'PRAGMA foreign_keys = ON',
            'add': f'INSERT INTO {self.table_name} ({names}) VALUES ({placeholders})',
            'get': f'SELECT ROWID, * FROM {self.table_name} WHERE ROWID = ?',
            'get_all': f'SELECT ROWID, * FROM {self.table_name}',
            'update': f'UPDATE {self.table_name} SET {fields_update} WHERE ROWID = ?',
            'delete': f'DELETE FROM {self.table_name} WHERE ROWID = ?',
        }

        # queries

    def _row2obj(self, row: tuple[Any]) -> Any:
        class_arguments = {}

        # Компановка аргументов класса (+ обработка формата datetime)
        for field_value, field_name in zip(row[1:], self.fields.keys()):    # type: ignore
            if self.fields[field_name] == datetime:
                field_value = datetime.strptime(field_value, DEFAULT_DATE_FORMAT)

            class_arguments[field_name] = field_value

        obj = self.cls(**class_arguments)
        obj.pk = row[0]

        return obj

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'Try to add object {obj} with filled `pk` attribute')

        values = [getattr(obj, x) for x in self.fields]

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.queries['foreign_keys'])
            cur.execute(self.queries['add'], values)

            if cur.lastrowid is not None:
                obj.pk = cur.lastrowid

        con.close()

        return obj.pk

    def get(self, pk: int) -> Any | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            row = cur.execute(self.queries['get'], [pk]).fetchone()

        con.close()

        if row is None:
            return None

        return self._row2obj(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            base = self.queries['get_all']

            if where is not None:
                conditions = " AND ".join([f"{field} = ?" for field in where.keys()])
                rows = cur.execute(
                    base + f' WHERE {conditions}',
                    list(where.values())
                ).fetchall()
            else:
                rows = cur.execute(base).fetchall()

        con.close()

        return [self._row2obj(row) for row in rows]

    def update(self, obj: T) -> None:
        if getattr(obj, 'pk', None) is None:
            raise ValueError('Try to update object without `pk` attribute')

        values = [getattr(obj, x) for x in self.fields]
        values.append(obj.pk)

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.queries['foreign_keys'])
            cur.execute(self.queries['update'], values)
            if cur.rowcount == 0:
                raise ValueError('Try to update object with unknown primary key')

        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.queries['delete'], [pk])
            if cur.rowcount == 0:
                raise ValueError('Try to delete object with unknown primary key')

        con.close()
