import random

from uuid import uuid4
from src.transaction.application.dto.transaction_response import TransactionResponse
from src.transaction.application.dto.transaction_request import TransactionRequest
from src.transaction.domain.model.Transaction import Transaction
from src.transaction.application.mapper import TransactionMapper
class TransactionUseCases:
    def __init__(self, transaction_input_port):
        self.transaction_input_port = transaction_input_port

    def create_transaction(self, transaction_data: TransactionRequest) -> TransactionResponse:
        transaction = TransactionMapper.request_to_domain(transaction_data)

        return TransactionMapper.domain_to_response(transaction)

    def get_transaction(self, transaction_id: str) -> TransactionResponse:
        # TODO: Implement repository to get data
        transaction = Transaction(
            id=str(uuid4()),
            amount=random.randint(1, 9999),
            description="Sample transaction"
        )
        return TransactionMapper.domain_to_response(transaction)