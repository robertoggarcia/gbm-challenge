import json
from os import getenv
from typing import Generic, Optional, TypeVar

import redis  # type: ignore[import]
from loguru import logger

from app.utils.exceptions import InMemoryManagerConnectionError

T = TypeVar("T")
S = TypeVar("S")


class InMemoryManager(Generic[T, S]):
    """Generic in memory class to manage redis connection and operations"""

    salt: str
    lifetime: int

    def __init__(self):
        try:
            self._redis = redis.StrictRedis(host=getenv("REDIS_HOST"))
        except redis.ConnectionError:
            logger.error("Failed to connect to Redis")
            raise InMemoryManagerConnectionError
        logger.debug(f"Redis running {self._redis}")

    def set(self, key: T, value: S) -> None:
        json_data = json.dumps(value)
        self._redis.set(f"{self.salt}_{key}", json_data, ex=self.lifetime)

    def get(self, key: T) -> Optional[S]:
        value = self._redis.get(f"{self.salt}_{key}")
        value = json.loads(value) if value else value
        return value
