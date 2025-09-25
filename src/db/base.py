from enum import Enum
from typing import Protocol


class SortOrder(Enum):
    ASC = 1
    DESC = -1


class IClient(Protocol):
    @classmethod
    def get_db(cls):
        raise NotImplementedError


class ICollection(Protocol):
    def insert_one(self, document: dict):
        raise NotImplementedError

    def insert_many(self, documents: list):
        raise NotImplementedError

    def find_one(self, query: dict, columns: list):
        raise NotImplementedError

    def find_many(self, query: dict, columns: list, sort=None, limit=None, skip=None) -> list:
        raise NotImplementedError

    def update_one(self, query: dict, to: dict) -> int:
        raise NotImplementedError

    def update_many(self, query: dict, to: dict) -> int:
        raise NotImplementedError

    # TODO: Need to implement transaction feature as well


def get_db(client: IClient):
    return client.get_db()


def get_table(name: str, collection_class: ICollection):
    return collection_class(name)
