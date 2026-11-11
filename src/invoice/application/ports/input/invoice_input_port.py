
from typing import Protocol
from invoice.application.dto.invoice_response import InvoiceRequest, InvoiceResponse

class InvoiceInputPort(Protocol):
    def create_invoice(self, invoice_data: InvoiceRequest) -> InvoiceResponse:
        ...