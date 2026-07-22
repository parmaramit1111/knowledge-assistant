from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Command(ABC, Generic[T]):

    @abstractmethod
    def execute(self) -> T:
        pass