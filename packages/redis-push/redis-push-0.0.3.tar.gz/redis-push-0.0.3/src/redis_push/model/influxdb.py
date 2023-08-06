from dataclasses import dataclass, field
from datetime import datetime
from typing import Union


@dataclass
class Point:
    measurement: str
    fields: dict[str, Union[str, int, float, bool]]
    tags: dict[str, str] = field(default_factory=dict)
    time: Union[datetime, str, int, None] = field(default=None)


@dataclass
class Points:
    bucket: str
    records: list[Point]
