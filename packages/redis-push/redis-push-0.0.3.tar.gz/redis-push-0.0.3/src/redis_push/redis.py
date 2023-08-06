import json
from dataclasses import asdict, is_dataclass
from typing import Union

import aioredis
from pydantic import BaseModel, BaseSettings, RedisDsn


class Env(BaseSettings):
    redis_dsn: RedisDsn

    class Config:
        env_file = ".env"


env = Env()


def convert_json(value):
    v = value
    if is_dataclass(value):
        v = asdict(value)
    if isinstance(value, BaseModel):
        v = value.dict()
    return json.dumps(v)


class RedisList:
    def __init__(self):
        self.redis = aioredis.Redis.from_url(env.redis_dsn)

    async def lpush(self, key: str, *values: Union[BaseModel, dict]):
        values = [convert_json(v) for v in values]
        await self.redis.lpush(key, *values)

    async def brpop(self, key: str):
        async with self.redis as r:
            res = await r.brpop(key)
        return res[1].decode()

    async def close(self):
        await self.redis.close()
