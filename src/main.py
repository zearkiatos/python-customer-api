from typing import Annotated

from fastapi import Depends, FastAPI
from src.core.dependencies import get_customer_use_cases
from src.customer.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.application.dto.customer_create_request import CustomerCreateRequest
from src.customer.application.dto.customer_response import CustomerResponse
from src.invoice.application.dto.invoice_request import InvoiceRequest
from src.transaction.application.dto.transaction_request import TransactionRequest
from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.invoice.infrastructure.adapters.transaction_lookup_adapter import TransactionLookupAdapter
from src.invoice.application.InvoiceUseCases import InvoiceUseCases


app = FastAPI()
in_memory_customer_repository = InMemoryCustomerRepository()
CustomerUseCasesDep = Annotated[CustomerUseCases, Depends(get_customer_use_cases)]
@app.post('/customers', response_model=CustomerResponse)
async def create_customer(customer: CustomerCreateRequest, customer_use_cases: CustomerUseCasesDep = Depends(get_customer_use_cases)):
    customer_validated = CustomerCreateRequest.model_validate(customer.model_dump())
    return customer_use_cases.create_customer(customer_validated)

@app.get('/customers', response_model=list[CustomerResponse])
async def get_customers(customer_use_cases: CustomerUseCasesDep = Depends(get_customer_use_cases)):
    return customer_use_cases.get_customers()

@app.post('/transactions')
async def create_transaction(transaction: TransactionRequest):
    transaction_use_cases = TransactionUseCases(None)
    return transaction_use_cases.create_transaction(transaction)

@app.post('/invoices')
async def create_invoice(invoice: InvoiceRequest):
    invoice_use_cases = InvoiceUseCases(None,TransactionLookupAdapter(TransactionUseCases(None)))
    return invoice_use_cases.create_invoice(invoice)