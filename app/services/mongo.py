from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> Optional[MongoClient]:
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    return MongoClient(uri)


def get_database():
    client = get_mongo_client()
    if client is None:
        return None
    db_name = os.getenv("MONGO_DB", "tripper")
    return client[db_name]
