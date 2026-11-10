from fastapi import FastAPI
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.application.dto.customer_request import CustomerRequest
from src.invoice.application.dto.invoice_request import InvoiceRequest
from src.transaction.application.dto.transaction_request import TransactionRequest
from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.invoice.application.InvoiceUseCases import InvoiceUseCases


app = FastAPI()
@app.post('/customers')
async def create_customer(customer: CustomerRequest):
    customer_use_cases = CustomerUseCases(None)
    return customer_use_cases.create_customer(customer)

@app.post('/transactions')
async def create_transaction(transaction: TransactionRequest):
    transaction_use_cases = TransactionUseCases(None)
    return transaction_use_cases.create_transaction(transaction)

@app.post('/invoices')
async def create_invoice(invoice: InvoiceRequest):
    invoice_use_cases = InvoiceUseCases(None)
    return invoice_use_cases.create_invoice(invoice)