from typing import Protocol

class CustomerLookupOutputPort(Protocol):
    def customer_exists(self, id: str) -> bool:
        ...