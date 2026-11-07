from fastapi import FastAPI
from .customer.application.dto.customer_request import CustomerRequest
from .transaction.application.dto.transaction_request import TransactionRequest
from .invoice.application.dto.invoice_request import InvoiceRequest


app = FastAPI()
@app.post('/customers')
async def create_customer(customer: CustomerRequest):
    return customer