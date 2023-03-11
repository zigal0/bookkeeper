"""
Модель категории расходов
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator
from bookkeeper.repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов.
    name - название категории
    parent_id - id родительской категории
    pk - id записи в базе данных
    """
    name: str = ''
    parent_id: int | None = None
    pk: int = 0

    def get_parent(self,
                   repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Returns
        -------
        Объект класса Category или None
        """
        if self.parent_id is None:
            return None
        return repo.get(self.parent_id)

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> Iterator['Category']:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self,
                          repo: AbstractRepository['Category']
                          ) -> Iterator['Category']:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent_id].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
            cls,
            tree: list[tuple[str, str | None]],
            repo: AbstractRepository['Category']) -> list['Category']:
        """
        Создать дерево категорий из списка пар "потомок-родитель".
        Список должен быть топологически отсортирован, т.е. потомки
        не должны встречаться раньше своего родителя.
        Проверка корректности исходных данных не производится.
        При использовании СУБД с проверкой внешних ключей, будет получена
        ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        со стороны СУБД, результат, возможно, будет корректным, если исходные
        данные корректны за исключением сортировки. Если нет, то нет.
        "Мусор на входе, мусор на выходе".

        Parameters
        ----------
        tree - список пар "потомок-родитель"
        repo - репозиторий для сохранения объектов

        Returns
        -------
        Список созданных объектов Category
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            category = cls(
                name=child,
                parent_id=created[parent].pk if parent is not None else None)
            repo.add(category)
            created[child] = category
        return list(created.values())
