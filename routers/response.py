from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    description: str
    data: T

