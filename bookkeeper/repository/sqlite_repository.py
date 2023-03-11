"""
Модуль описывает репозиторий, работающий с СУБД SQLite.
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from datetime import datetime, date


from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """Основной репозиторий для работы с СУБД SQLite."""

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
            'get': f'SELECT pk, {names} FROM {self.table_name} WHERE pk = ?',
            'get_all': f'SELECT pk, {names}  FROM {self.table_name}',
            'update': f'UPDATE {self.table_name} SET {fields_update} WHERE pk = ?',
            'delete': f'DELETE FROM {self.table_name} WHERE pk = ?',
        }

    def _row2obj(self, row: tuple[Any]) -> T:
        """Just a soul cry: dynamic typing is shit"""
        class_arguments = {}

        # Компановка аргументов класса (+ обработка формата datetime, date)
        for field_value, field_name in zip(row[1:], self.fields.keys()):    # type: ignore
            if self.fields[field_name] == datetime:
                field_value = datetime.fromisoformat(field_value)

            if self.fields[field_name] == date:
                field_value = date.fromisoformat(field_value)

            class_arguments[field_name] = field_value

        obj = self.cls(**class_arguments)
        obj.pk = row[0]

        return obj  # type: ignore

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

    def get(self, pk: int) -> T | None:
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
            cur.execute(self.queries['foreign_keys'])
            cur.execute(self.queries['delete'], [pk])
            if cur.rowcount == 0:
                raise ValueError('Try to delete object with unknown primary key')

        con.close()
