from src.transaction.application.dto.transaction_response import TransactionResponse
from src.transaction.application.errorHandler.customer_not_found_exception import CustomerNotFoundException
from src.transaction.application.dto.transaction_request import TransactionRequest
from src.transaction.application.mapper import TransactionMapper
from src.transaction.domain.repositories.transaction_repository import TransactionRepository
from src.transaction.application.ports.output.customer_lookup_output_port import CustomerLookupOutputPort
class TransactionUseCases:
    def __init__(self, transaction_input_port, transaction_repository: TransactionRepository, customer_lookup_port: CustomerLookupOutputPort):
        self.transaction_input_port = transaction_input_port
        self.transaction_repository = transaction_repository
        self.customer_lookup_port = customer_lookup_port

    def create_transaction(self, transaction_data: TransactionRequest) -> TransactionResponse:
        customer_exists = self.customer_lookup_port.customer_exists(transaction_data.customer_id)
        if not customer_exists:
            raise CustomerNotFoundException(transaction_data.customer_id)
    
        transaction = TransactionMapper.request_to_domain(transaction_data)
        transaction_updated = self.transaction_repository.save(transaction)

        return TransactionMapper.domain_to_response(transaction_updated)

    def get_transaction(self, transaction_id: str) -> TransactionResponse:
        transaction = self.transaction_repository.get_by_id(transaction_id)
        if transaction is None:
            raise ValueError(f"Transaction with id {transaction_id} not found")
        return TransactionMapper.domain_to_response(transaction)

    def get_transactions(self) -> list[TransactionResponse]:
        transactions = self.transaction_repository.get()
        return [TransactionMapper.domain_to_response(t) for t in transactions]
