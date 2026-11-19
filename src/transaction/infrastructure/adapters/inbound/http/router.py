
from fastapi import APIRouter

from src.invoice.application import InvoiceUseCases
from src.invoice.application.dto.invoice_request import InvoiceRequest
from src.invoice.infrastructure.adapters.transaction_lookup_adapter import TransactionLookupAdapter
from src.transaction.application import TransactionUseCases

router = APIRouter()

@router.post('/invoices', tags=["invoice"])
async def create_invoice(invoice: InvoiceRequest):
    invoice_use_cases = InvoiceUseCases(None,TransactionLookupAdapter(TransactionUseCases(None)))
    return invoice_use_cases.create_invoice(invoice)