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

        # queries
        self.query_foreign_keys = 'PRAGMA foreign_keys = ON'
        self.query_add = f'INSERT INTO {self.table_name} ({names}) VALUES ({placeholders})'
        self.query_get = f'SELECT ROWID, * FROM {self.table_name} WHERE ROWID = ?'
        self.query_get_all = f'SELECT ROWID, * FROM {self.table_name}'
        self.query_update = f'UPDATE {self.table_name} SET {fields_update} WHERE ROWID = ?'
        self.query_delete = f'DELETE FROM {self.table_name} WHERE ROWID = ?'

    def _row2obj(self, row: tuple[Any]) -> T:
        kwargs = dict(zip(self.fields, row[1:]))
        obj = self.cls(**kwargs)
        obj.pk = row[0]

        # Приводим время к требуемому формату
        for filed_name, field_cls in self.fields.items():
            print(field_cls)
            if field_cls == datetime:
                date_str = obj.__getattribute__(filed_name)
                date_format = datetime.strptime(date_str, DEFAULT_DATE_FORMAT)
                obj.__setattr__(filed_name, date_format)

        return obj

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'try to add object {obj} with filled `pk` attribute')

        values = [getattr(obj, x) for x in self.fields]

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.query_foreign_keys)
            cur.execute(self.query_add, values)
            obj.pk = cur.lastrowid

        con.close()

        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            row = cur.execute(self.query_get, [pk]).fetchone()

        con.close()

        if row is None:
            return None

        return self._row2obj(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            if where is not None:
                conditions = " AND ".join([f"{field} = ?" for field in where.keys()])
                rows = cur.execute(
                    self.query_get_all + f' WHERE {conditions}',
                    list(where.values())
                ).fetchall()
            else:
                rows = cur.execute(self.query_get_all).fetchall()

        con.close()

        return [self._row2obj(row) for row in rows]

    def update(self, obj: T) -> None:
        if getattr(obj, 'pk', None) is None:
            raise ValueError(f'try to update object without `pk` attribute')

        values = [getattr(obj, x) for x in self.fields]
        values.append(obj.pk)

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.query_foreign_keys)
            cur.execute(self.query_update, values)
            if cur.rowcount == 0:
                raise ValueError('Try to update object with unknown primary key')

        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(self.query_delete, [pk])
            if cur.rowcount == 0:
                raise ValueError('Try to delete object with unknown primary key')

        con.close()
