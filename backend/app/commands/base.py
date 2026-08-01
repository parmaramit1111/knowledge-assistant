from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Command(ABC, Generic[T]):

    @abstractmethod
    async def execute(self) -> T:
        """Execute the command."""
        raise NotImplementedError