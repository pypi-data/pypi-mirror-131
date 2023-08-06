import aioredis
from pydantic import BaseSettings, RedisDsn, BaseModel
import json
from typing import Union


class Env(BaseSettings):
    redis_dsn: RedisDsn

    class Config:
        env_file = ".env"


env = Env()


class RedisList:
    def __init__(self):
        self.redis = aioredis.Redis.from_url(env.redis_dsn)

    async def lpush(self, key: str, *values: Union[BaseModel, dict]):
        values = [
            json.dumps(v.dict() if isinstance(v, BaseModel) else v) for v in values
        ]
        await self.redis.lpush(key, *values)

    async def brpop(self, key: str):
        async with self.redis as r:
            res = await r.brpop(key)
        return res[1].decode()

    async def close(self):
        await self.redis.close()
