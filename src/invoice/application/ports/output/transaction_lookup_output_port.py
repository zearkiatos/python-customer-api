from abc import ABC, abstractmethod

class TransactionLookupOutputPort(ABC):
    @abstractmethod
    def get_amounts(self, transaction_ids: list[str]) -> dict[str, int]:
        ...