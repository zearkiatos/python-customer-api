
from typing import Protocol
from transaction.application.dto.transaction_response import TransactionResponse
from transaction.application.dto.transaction_request import TransactionRequest

class TransactionInputPort(Protocol):
    def create_transaction(self, transaction_data: TransactionRequest) -> TransactionResponse:
        ...