import pytest
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from bookkeeper.repository.sqlite_repository import SQLiteRepository

DB_FILE = "bookkeeper_test.db"
FIELD_INT = 1337
FILED_STR = "smth"
FIELD_DATE = datetime.now()


@pytest.fixture
def create_schema():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS custom")

    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS custom(field_int int, field_str int, field_date text)")
    con.close()


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        field_int: int = FIELD_INT
        field_str: str = FILED_STR
        field_date: datetime = FIELD_DATE
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class, create_schema):
    return SQLiteRepository(db_file=DB_FILE, cls=custom_class)


def test__row2obj(repo):
    pk = 1

    row = (pk, FIELD_INT, FILED_STR, str(FIELD_DATE))
    obj = repo._row2obj(row)
    assert obj.pk == pk
    assert obj.field_int == FIELD_INT
    assert obj.field_str == FILED_STR
    assert obj.field_date == FIELD_DATE


def test_crud(repo, custom_class):
    # add
    obj_add = custom_class()
    pk = repo.add(obj_add)
    assert pk == obj_add.pk

    # get
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == obj_add.pk
    assert obj_get.field_int == obj_add.field_int
    assert obj_get.field_str == obj_add.field_str
    assert obj_get.field_date == obj_add.field_date

    # update
    obj_update = custom_class(2022, "smth_new", datetime.now(), pk)
    repo.update(obj_update)
    obj_get = repo.get(pk)
    assert obj_get.pk == obj_update.pk
    assert obj_get.field_int == obj_update.field_int
    assert obj_get.field_str == obj_update.field_str
    assert obj_get.field_date == obj_update.field_date

    # delete
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_filled_pk(repo, custom_class):
    obj = custom_class(pk=1)
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk_property(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_update_nonexistent(repo, custom_class):
    obj = custom_class(pk=2)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_without_pk_property(repo, custom_class):
    with pytest.raises(ValueError):
        repo.update(0)


def test_get_nonexistent(repo):
    assert repo.get(-1) is None


def test_cannot_delete_nonexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(-1)


def test_get_all(repo, custom_class):
    objs = [custom_class() for _ in range(5)]
    for obj in objs:
        repo.add(obj)
    objs_pk = [obj.pk for obj in objs]
    objs_get_all_pk = [obj.pk for obj in repo.get_all()]
    assert objs_pk == objs_get_all_pk


def test_get_all_with_condition(repo, custom_class):
    objs = []
    for i in range(5):
        obj = custom_class(field_int=i)
        repo.add(obj)
        objs.append(obj)
    res = repo.get_all({'field_int': 0})
    assert res == [objs[0]]
    assert repo.get_all({'field_str': FILED_STR}) == objs
