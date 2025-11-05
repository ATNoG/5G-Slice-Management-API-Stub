# -*- coding: utf-8 -*-
# @Author: Miguel Figueiredo
# @Date:   2025-11-05 16:42:57
# @Last Modified by:   Miguel Figueiredo
# @Last Modified time: 2025-11-05 16:42:57

from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    description: str
    data: T

