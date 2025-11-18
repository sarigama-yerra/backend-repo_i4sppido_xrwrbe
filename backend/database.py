import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[MongoClient] = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

# Helpers that auto-add timestamps

def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    db = get_db()
    now = datetime.utcnow()
    data = {**data, "created_at": now, "updated_at": now}
    result = db[collection_name].insert_one(data)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = get_db()
    cur = db[collection_name].find(filter_dict or {}).limit(limit)
    out = []
    for d in cur:
        d["_id"] = str(d.get("_id"))
        out.append(d)
    return out
