from src.db import COLLECTIONS, INDICES, VALIDATORS, MongoDBClient, get_db


def create_collection():
    db = get_db(MongoDBClient)
    existing_collections = db.list_collection_names()
    for name in COLLECTIONS:
        validator = VALIDATORS.get(name)
        indices = INDICES.get(name)
        try:
            if name in existing_collections:
                continue
            collection = db.create_collection(
                name, validator=validator, validationLevel="strict", validationAction="error"
            )
            collection.create_indexes(indices)
        except Exception as e:
            print(e)


def migrate_collection():
    db = get_db(MongoDBClient)
    existing_collections = db.list_collection_names()
    for name in existing_collections:
        validator = VALIDATORS.get(name)
        indices = INDICES.get(name)
        try:
            db.command(
                "collMod", name, validator=validator, validationLevel="strict", validationAction="error"
            )
            db[name].create_indexes(indices)
        except Exception as e:
            print(e)
