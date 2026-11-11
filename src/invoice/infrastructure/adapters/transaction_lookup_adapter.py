from src.invoice.application.ports.output.transaction_lookup_output_port import TransactionLookupOutputPort
from src.transaction.application.ports.input.TransactionInputPort import TransactionInputPort

class TransactionLookupAdapter(TransactionLookupOutputPort):
    def __init__(self, transaction_port: TransactionInputPort):
        self.transaction_port = transaction_port
    def get_amounts(self, transaction_ids: list[str]) -> dict[str, int]:
        amounts = {}
        for id in transaction_ids:
            transaction = self.transaction_port.get_transaction(id)

            amounts[id] = int(transaction.amount)

        return amounts