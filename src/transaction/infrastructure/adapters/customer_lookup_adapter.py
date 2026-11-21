from src.customer.application.ports.input.customer_input_port import CustomerInputPort
from src.transaction.application.ports.output.customer_lookup_output_port import CustomerLookupOutputPort


class CustomerLookupAdapter(CustomerLookupOutputPort):
    def __init__(self, customer_port: CustomerInputPort):
        self.customer_port = customer_port

    def customer_exists(self, id: str) -> bool:
        try:
            return self.customer_port.get_customer_by_id(id) is not None
        except ValueError:
            return False