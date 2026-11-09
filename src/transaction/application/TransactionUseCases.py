
from ...transaction.application.dto.transaction_response import TransactionResponse
from ...transaction.application.dto.transaction_request import TransactionRequest
from ...transaction.application.mapper.TransactionMapper import TransactionMapper

class TransactionUseCases:
    def __init__(self, transaction_input_port):
        self.transaction_input_port = transaction_input_port

    def create_transaction(self, transaction_data: TransactionRequest) -> TransactionResponse:
        transaction = TransactionMapper.request_to_domain(transaction_data)
        return self.transaction_input_port.create_transaction(transaction)