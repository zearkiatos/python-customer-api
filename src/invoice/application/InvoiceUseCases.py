from src.invoice.application.dto.invoice_response import InvoiceResponse
from src.invoice.application.dto.invoice_request import InvoiceRequest
from src.invoice.application.mapper import InvoiceMapper

class InvoiceUseCases:
    def __init__(self, invoice_input_port, transaction_lookup_port):
        self.invoice_input_port = invoice_input_port
        self.transaction_lookup_port = transaction_lookup_port

    def create_invoice(self, invoice_data: InvoiceRequest) -> InvoiceResponse:
        amounts = self.transaction_lookup_port.get_amounts([str(t) for t in invoice_data.transactions])
        invoice = InvoiceMapper.request_to_domain(invoice_data, amounts)
        return InvoiceMapper.domain_to_response(invoice)