from typing import List, Tuple

from pymongo import MongoClient

from src.db import SortOrder
from src.helpers import utc_now
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
        if name not in self.db.list_collection_names():
            raise ValueError(f"Provided '{name}' collection not found in DB.")

    def insert_one(self, document: dict):
        now = utc_now()
        document.update({
            "created_at": now,
            "is_active": True,
            "modified_at": now
        })
        return self.collection.insert_one(document=document).inserted_id


    def insert_many(self, documents: list[dict]):
        now = utc_now()
        for doc in documents:
            doc.update({
                "created_at": now,
                "is_active": True,
                "modified_at": now
            })
        return self.collection.insert_many(documents=documents).inserted_ids


    def find_one(self, query: dict, columns: list=None, sort: List[Tuple]=None, ignore_defaults:bool=False):
        projection = {col: 1 for col in columns} if columns else {}

        # NOTE: to prevent inclusion on field in exclusion projection
        if not projection and ignore_defaults:
            projection.update({"_id": 0, "created_at": 0, "modified_at": 0, "is_active": 0})

        if sort:
            sort_keys = [(field, 1 if direction == SortOrder.ASC else -1) for field, direction in sort]
            return self.collection.find_one(query, sort=sort_keys, projection=projection)

        return self.collection.find_one(query, projection)

    def find_many(
            self, query: dict, sort: List[Tuple]=None, limit=None, skip=None, columns: list=None, ignore_defaults:bool=False
    ) -> list:
        projection = {col: 1 for col in columns} if columns else {}

        # NOTE: to prevent inclusion on field in exclusion projection
        if not projection and ignore_defaults:
            projection.update({"_id": 0, "created_at": 0, "modified_at": 0, "is_active": 0})

        cursor = self.collection.find(query, projection)

        if sort:
            sort_keys = [(field, 1 if direction == SortOrder.ASC else -1) for field, direction in sort]
            cursor = cursor.sort(sort_keys)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def update_one(self, query: dict, update: dict) -> int:
        if "$set" in update:
            update["$set"]["modified_at"] = utc_now()
        else:
            update["$set"] = {"modified_at": utc_now()}
        result = self.collection.update_one(query, update)
        return result.modified_count

    def update_many(self, query: dict, update: dict) -> int:
        if "$set" in update:
            update["$set"]["modified_at"] = utc_now()
        else:
            update["$set"] = {"modified_at": utc_now()}
        result = self.collection.update_many(query, update)
        return result.modified_count

    def delete_one(self, query:dict):
        return self.collection.update(query, {"$set": {"is_active": False, "modified_at": utc_now()}}).modified_count

    def delete_many(self, query:dict):
        return self.collection.update_many(query, {"$set": {"is_active": False, "modified_at": utc_now()}}).modified_count

    def hard_delete(self, query:dict):
        return self.collection.delete_one(query).deleted_count

    def hard_delete_many(self, query:dict):
        return self.collection.delete_many(query).deleted_count

    def count(self, query:dict):
        if not query:
            query = {}
        return self.collection.count_documents(query)

    def active_count(self, query: dict):
        if "is_active" not in query:
            query.update({"is_active": True})
        return self.collection.count_documents(query)
