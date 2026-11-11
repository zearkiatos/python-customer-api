from dataclasses import dataclass

@dataclass(frozen=True)

class Transaction:
    transaction_id: str
    amount: int