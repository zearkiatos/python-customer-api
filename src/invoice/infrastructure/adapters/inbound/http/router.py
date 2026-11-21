from fastapi import APIRouter

from src.invoice.application.dto.invoice_request import InvoiceRequest
from src.invoice.application.InvoiceUseCases import InvoiceUseCases

router = APIRouter()

@router.post('/invoices', tags=["invoice"])
async def create_invoice(invoice: InvoiceRequest):
    invoice_use_cases = InvoiceUseCases(None, None)
    return invoice_use_cases.create_invoice(invoice)