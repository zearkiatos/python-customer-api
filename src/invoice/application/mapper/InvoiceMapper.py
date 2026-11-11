from uuid import uuid4

from ...application.dto.invoice_request import InvoiceRequest
from ...application.dto.invoice_response import InvoiceResponse
from ...domain.model.Invoice import Invoice
from ...domain.model.Transaction import Transaction

def request_to_domain(request: InvoiceRequest, amounts: dict[str, int]) -> Invoice:
    id = uuid4()
    transactions = []
    for t in request.transactions:
        tid = str(t) # excepción de dominio
        transactions.append(Transaction(transaction_id=tid, amount=amounts[tid]))
    return Invoice(
        id=str(id),
        name=request.name,
        customer_id=str(request.customer_id),
        transactions=transactions
    )

def domain_to_response(domain: Invoice) -> InvoiceResponse:
    return InvoiceResponse(
        id=domain.id,
        name=domain.name,
        customer_id=domain.customer_id,
        transactions=[t.transaction_id for t in domain.transactions],
        total=domain.total
    )