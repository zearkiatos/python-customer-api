from invoice.application.dto.invoice_response import InvoiceRequest, InvoiceResponse
from invoice.application.mapper.InvoiceMapper import InvoiceMapper

class InvoiceUseCases:
    def __init__(self, invoice_input_port):
        self.invoice_input_port = invoice_input_port

    def create_invoice(self, invoice_data: InvoiceRequest) -> InvoiceResponse:
        invoice = InvoiceMapper.request_to_domain(invoice_data)
        return self.invoice_input_port.create_invoice(invoice)