from abc import ABC, abstractmethod
from typing import Any, TypeVar
from ..events import SQSEvent, SNSEvent, S3ObjectLambdaEvent, SimpleEmailEvent
from .icontext import IContext
from pydantic import validate_arguments

Event = TypeVar(
    "Event",
    SQSEvent,
    SNSEvent,
    S3ObjectLambdaEvent,
    SimpleEmailEvent,
)


class IHandler(ABC):
    @staticmethod
    @validate_arguments
    @abstractmethod
    def handler(event: Event, context: IContext) -> Any:
        ...
