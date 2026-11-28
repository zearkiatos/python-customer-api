from typing import Annotated
from http import HTTPStatus as HttpStatus
from fastapi import Depends, HTTPException, APIRouter

from src.core.dependencies import get_customer_use_cases
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.application.dto.customer_create_request import CustomerCreateRequest
from src.customer.application.dto.customer_plan_response import CustomerPlanResponse
from src.customer.application.dto.customer_response import CustomerResponse
from src.customer.application.dto.subscribe_customer_plan_request import SubscribeCustomerPlanRequest
from src.customer.application.dto.subscribe_customer_plan_update import SubscribeCustomerPlanUpdate
from src.customer.application.errorHandler.PlanNotFoundException import PlanNotFoundException

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

@router.post('/customers/{customer_id}/plans/{plan_id}', status_code=HttpStatus.CREATED, tags=["customer"])
async def subscribe_to_plan(customer_id: str, plan_id: str, customer_use_cases: CustomerUseCasesDep):
    try:
        subscribe_plan_request = SubscribeCustomerPlanRequest(customer_id=customer_id, plan_id=plan_id)
        subscribe_validated = SubscribeCustomerPlanRequest.model_validate(subscribe_plan_request.model_dump())
        return customer_use_cases.subscribe_customer_to_plan(subscribe_validated)
    except PlanNotFoundException as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HttpStatus.INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/customers/{customer_id}/plans', response_model=list[CustomerPlanResponse], tags=["customer"])
async def get_plans_by_customer_id(customer_id: str, customer_use_cases: CustomerUseCasesDep):
    try:
        return customer_use_cases.get_plans_by_customer_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))

@router.get('/customers/{customer_id}/plans/{state}', response_model=list[CustomerPlanResponse], tags=["customer"])
async def get_plans_by_customer_id_and_state(customer_id: str, state: str, customer_use_cases: CustomerUseCasesDep):
    try:
        return customer_use_cases.get_plans_by_customer_id_and_state(customer_id, state)
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))

@router.patch('/customers/{customer_id}/plans/{plan_id}', status_code=HttpStatus.OK, tags=["customer"])
async def update_subscription_state(plan_update: SubscribeCustomerPlanUpdate, customer_id: str, plan_id: str, customer_use_cases: CustomerUseCasesDep):
    try:
        return customer_use_cases.subscribe_customer_plan_update(customer_id, plan_id, plan_update)
    except ValueError as e:
        raise HTTPException(status_code=HttpStatus.NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HttpStatus.INTERNAL_SERVER_ERROR, detail=str(e))
