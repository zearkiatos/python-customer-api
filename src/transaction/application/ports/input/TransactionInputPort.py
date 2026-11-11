
from typing import Protocol
from src.transaction.application.dto.transaction_response import TransactionResponse
from src.transaction.application.dto.transaction_request import TransactionRequest

class TransactionInputPort(Protocol):
    def create_transaction(self, transaction_data: TransactionRequest) -> TransactionResponse:
        ...

    def get_transaction(self, transaction_id: str) -> TransactionResponse:
        ...