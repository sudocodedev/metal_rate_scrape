from pymongo import IndexModel

COLLECTIONS = ["user", "insight", "metal_rate", "job_tracker"]

VALIDATORS = {
    "user": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "phone_number", "gender", "city"],
            "properties": {
                "first_name": {"bsonType": "string"},
                "last_name": {"bsonType": "string"},
                "phone_number": {"bsonType": "string", "pattern": "^[6-9][0-9]{9}$"},
                "gender": {"enum": ["male", "female", "other"]},
                "area": {"bsonType": "string"},
                "city": {"bsonType": "string"},
                "created_at": {"bsonType": "date"},
                "modified_at": {"bsonType": "date"},
                "is_active": {"bsonType": "bool"},
            },
        }
    },
    "metal_rate": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["date", "type", "price_per_g", "diff", "percent", "source"],
            "oneOf": [
                {
                    "properties": {"type": {"enum": ["gold"]}, "purity": {"enum": ["22k", "24k"]}},
                    "required": ["purity"],
                },
                {"properties": {"type": {"enum": ["silver"]}}},
            ],
            "properties": {
                "date": {"bsonType": "date"},
                "price_per_g": {"bsonType": "double"},
                "diff": {"bsonType": "double"},
                "percent": {"bsonType": "double"},
                "source": {"bsonType": "string"},
                "created_at": {"bsonType": "date"},
                "modified_at": {"bsonType": "date"},
                "is_active": {"bsonType": "bool"},
            },
        }
    },
    "insight": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["type", "status", "delivered_count", "user_count", "message"],
            "properties": {
                "type": {"enum": ["daily", "weekly", "monthly", "yearly"]},
                "status": {"enum": ["success", "failure", "partial", "aborted"]},
                "delivered_count": {"bsonType": "int", "minimum": 0},
                "user_count": {"bsonType": "int", "minimum": 0},
                "message": {"bsonType": "string", "minLength": 20},
                "sent_at": {"bsonType": "date"},
                "reason": {"bsonType": "string", "maxLength": 512},
                "created_at": {"bsonType": "date"},
                "modified_at": {"bsonType": "date"},
                "is_active": {"bsonType": "bool"},
            },
        }
    },
    "job_tracker": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["scraped_at", "source", "status", "reason"],
            "properties": {
                "scraped_at": {"bsonType": "date"},
                "source": {"bsonType": "string"},
                "status": {"enum": ["success", "failure", "partial", "aborted"]},
                "reason": {"bsonType": "string", "maxLength": 512},
                "created_at": {"bsonType": "date"},
                "modified_at": {"bsonType": "date"},
                "is_active": {"bsonType": "bool"},
            },
        }
    },
}


INDICES = {
    "user": [
        IndexModel([("phone_number", 1)], unique=True),
        IndexModel([("city", 1), ("area", 1)]),
        IndexModel([("is_active", 1)]),
        IndexModel([("created_at", 1)]),
    ],
    "metal_rate": [
        IndexModel([("date", 1), ("source", 1), ("type", 1)], unique=True),
        IndexModel([("purity", 1)]),
        IndexModel([("is_active", 1)]),
        IndexModel([("created_at", 1)]),
    ],
    "insight": [
        IndexModel([("sent_at", 1)]),
        IndexModel([("type", 1)]),
        IndexModel([("status", 1)]),
        IndexModel([("is_active", 1)]),
        IndexModel([("created_at", 1)]),
    ],
    "job_tracker": [
        IndexModel([("scraped_at", 1)]),
        IndexModel([("source", 1)]),
        IndexModel([("status", 1)]),
        IndexModel([("is_active", 1)]),
        IndexModel([("created_at", 1)]),
    ],
}
