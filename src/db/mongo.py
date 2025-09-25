from pymongo import MongoClient

from src.db import SortOrder
from src.settings import DB, URI


class MongoDBClient:
    _client = None

    @classmethod
    def get_db(cls):
        if not cls._client:
            cls._client = MongoClient(URI)
        return cls._client[DB]


class MongoCollection:
    def __init__(self, name: str):
        self.db = MongoDBClient.get_db()
        self._validate_collection(name)
        self.collection = self.db[name]

    def _validate_collection(self, name):
        if name not in self.db._list_collection_names():
            raise Exception(f"Provided '{name}' collection not found in DB.")

    def insert_one(self, document: dict):
        return self.collection.insert_one(document=document).inserted_id

    def insert_many(self, documents: list):
        return self.collection.insert_many(documents=documents).inserted_ids

    def find_one(self, query: dict, columns: list):
        projection = {col: 1 for col in columns} if columns else None
        return self.collection.find_one(query, projection)

    def find_many(self, query: dict, columns: list, sort=None, limit=None, skip=None) -> list:
        projection = {col: 1 for col in columns} if columns else None
        cursor = self.collection.find(query, projection)

        if sort:
            sort_keys = [(field, 1 if direction == SortOrder.ASC else -1) for field, direction in sort]
            cursor = cursor.sort(sort_keys)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def update_one(self, query: dict, to: dict) -> int:
        result = self.collection.update_one(query, to)
        return result.modified_count

    def update_many(self, query: dict, to: dict) -> int:
        result = self.collection.update_many(query, to)
        return result.modified_count
