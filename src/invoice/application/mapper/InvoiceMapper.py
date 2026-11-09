from uuid import uuid4

from ...application.dto.invoice_request import InvoiceRequest
from ...application.dto.invoice_response import InvoiceResponse
from ...domain.model.Invoice import Invoice

def request_to_domain(request: InvoiceRequest) -> Invoice:
    id = uuid4()
    return Invoice(
        id=str(id),
        name=request.name,
        customer_id=str(request.customer_id),
        transactions=[str(transaction) for transaction in request.transactions]
    )

def domain_to_response(domain: Invoice) -> InvoiceResponse:
    return InvoiceResponse(
        id=domain.id,
        name=domain.name,
        customer_id=domain.customer_id,
        transactions=domain.transactions
    )