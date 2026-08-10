from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Query(ABC, Generic[T]):

    @abstractmethod
    def execute(self) -> T:
        """Execute the query."""
        raise NotImplementedError