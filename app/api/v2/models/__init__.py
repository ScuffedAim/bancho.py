# isort: dont-add-imports

from collections.abc import Mapping
from typing import Any
from typing import TypeVar

from pydantic import BaseModel as _pydantic_BaseModel
from pydantic import ConfigDict

T = TypeVar("T", bound="BaseModel")


class BaseModel(_pydantic_BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra="allow")

    @classmethod
    def from_mapping(cls: type[T], mapping: Mapping[str, Any]) -> T:
            print(mapping)
            return cls(**{k: mapping[k] for k in cls.model_fields})
