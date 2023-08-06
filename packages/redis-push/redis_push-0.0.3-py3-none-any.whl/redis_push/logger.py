import asyncio
from functools import wraps
from typing import Optional

from .model.slack import ErrorMessage, Message
from .model.influxdb import Point, Points
from .redis import RedisList


def create_task(func):
    @wraps(func)
    async def wrap(self: "Logger", *args, **kwargs):
        task = asyncio.create_task(func(self, *args, **kwargs))
        self.tasks.append(task)
        await asyncio.sleep(0)

    return wrap


class Logger:
    def __init__(self, channel: str = "test", error_channel: Optional[str] = None):
        self.channel = channel
        self.error_channel = channel if error_channel is None else error_channel
        self.redis = RedisList()
        self.tasks = []

    async def wait(self):
        await asyncio.wait(self.tasks)

    async def close(self):
        await self.wait()
        await self.redis.close()

    @create_task
    def error(self, origin: Optional[str] = None):
        em = ErrorMessage.from_exc_info(channel=self.error_channel, origin=origin)
        return self.redis.lpush("slack", em)

    @create_task
    def info(self, message: str, mention: bool = False):
        print(message)
        m = Message(channel=self.channel, message=message, mention=mention)
        return self.redis.lpush("slack", m)

    @create_task
    def points(self, bucket: str, points: list[Point]):
        ps = Points(bucket=bucket, records=points)
        return self.redis.lpush("influxdb", ps)
