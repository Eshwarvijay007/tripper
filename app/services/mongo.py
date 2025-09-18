from __future__ import annotations

import os
import logging
from functools import lru_cache
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError


@lru_cache(maxsize=1)
def get_mongo_client() -> Optional[MongoClient]:
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    # Create client, then verify connectivity. If it fails, fall back to None
    try:
        timeout_ms = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", "3000"))
        tls_kwargs = {}
        # Optionally use certifi CA bundle to avoid local cert store issues
        try:
            import certifi  # type: ignore

            tls_kwargs["tlsCAFile"] = certifi.where()
        except Exception:
            pass

        client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms, **tls_kwargs)
        # Force a quick server selection by doing a lightweight command
        client.admin.command("ping")
        return client
    except PyMongoError as e:
        logging.warning("Mongo unavailable, falling back to memory store: %s", e)
        return None


def get_database():
    client = get_mongo_client()
    if client is None:
        return None
    db_name = os.getenv("MONGO_DB", "tripper")
    return client[db_name]
