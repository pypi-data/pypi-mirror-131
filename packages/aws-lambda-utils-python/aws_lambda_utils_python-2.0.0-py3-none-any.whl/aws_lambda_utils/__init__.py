from pydantic import BaseModel
import typing


class BaseModelOptionalFields(BaseModel):
    def __init_subclass__(cls, *args, **kwargs) -> None:
        for field, value in cls.__annotations__.items():
            cls.__annotations__[field] = typing.Optional[value]
            if not hasattr(cls, field):
                setattr(cls, field, None)
        super().__init_subclass__(*args, **kwargs)
