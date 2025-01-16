from abc import ABCMeta, abstractmethod
from typing import AsyncGenerator


class IPatientRepository(metaclass=ABCMeta):
    @abstractmethod
    async def download_csv(self, limit: int | None) -> AsyncGenerator[list, None]:
        raise NotImplementedError
