import sys
import traceback
from typing import Literal, Optional, Union

from pydantic import BaseModel

Type = Literal["error", "message"]


class SlackBase(BaseModel):
    type: Type


class Message(SlackBase):
    type: Type = "message"
    channel: str
    message: str
    mention: bool = False


class Traceback(BaseModel):
    lineno: int
    line: str
    filename: str
    name: str
    locals: dict[str, str] = {}


class ErrorMessage(SlackBase):
    type: Type = "error"
    channel: str
    error_name: str
    message: str
    tracebacks: list[Traceback] = []
    origin: Optional[str]

    @classmethod
    def from_exc_info(cls, channel: str, origin: Optional[str]) -> "ErrorMessage":
        type_, value, tb = sys.exc_info()
        tracebacks: list[Traceback] = []
        for e in traceback.StackSummary.extract(
            traceback.walk_tb(tb), capture_locals=True
        ):
            tracebacks.append(
                Traceback(
                    lineno=e.lineno,
                    line=e.line,
                    filename="ipykernel" if "ipykernel_" in e.filename else e.filename,
                    name=e.name,
                    locals={
                        k: f"{v}"
                        for k, v in ([] if e.locals is None else e.locals.items())
                    },
                )
            )
        return cls(
            channel=channel,
            error_name=type_.__name__,
            message=f"{value}",
            tracebacks=tracebacks,
            origin=origin,
        )


Models = Union[ErrorMessage, Message]

mapping: dict[Type, Models] = {
    "error": ErrorMessage,
    "message": Message,
}
