from typing import Annotated
from http import HTTPStatus as HttpStatus
from fastapi import Depends, HTTPException, APIRouter

from src.core.dependencies import get_customer_use_cases
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.application.dto.customer_create_request import CustomerCreateRequest
from src.customer.application.dto.customer_response import CustomerResponse

router = APIRouter()

CustomerUseCasesDep = Annotated[CustomerUseCases, Depends(get_customer_use_cases)]
@router.post('/customers', response_model=CustomerResponse, tags=["customer"])
async def create_customer(customer: CustomerCreateRequest, customer_use_cases: CustomerUseCasesDep):
    customer_validated = CustomerCreateRequest.model_validate(customer.model_dump())
    return customer_use_cases.create_customer(customer_validated)

@router.get('/customers', response_model=list[CustomerResponse], tags=["customer"])
async def get_customers(customer_use_cases: CustomerUseCasesDep):
    return customer_use_cases.get_customers()

@router.get('/customers/{id}', response_model=CustomerResponse, tags=["customer"])
async def get_customer(id: str, customer_use_cases: CustomerUseCasesDep):
    try:
        return customer_use_cases.get_customer_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))

@router.delete('/customers/{id}', tags=["customer"])
async def delete_customer(id: str, customer_use_cases: CustomerUseCasesDep):
    try:
        customer_use_cases.delete_customer(id)
        return {"message": f"Customer with id {id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))

@router.patch('/customers/{id}', status_code=HttpStatus.CREATED, tags=["customer"])
async def update_customer(id: str, customer: CustomerCreateRequest, customer_use_cases: CustomerUseCasesDep):
    try:
        customer_validated = CustomerCreateRequest.model_validate(customer.model_dump())
        return customer_use_cases.update_customer(id, customer_validated)
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))