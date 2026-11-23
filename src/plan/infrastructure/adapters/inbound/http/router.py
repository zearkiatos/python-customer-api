from typing import Annotated
from http import HTTPStatus
from fastapi import Depends, HTTPException, APIRouter

from src.core.dependencies import get_plan_use_cases
from src.plan.application.PlanUseCases import PlanUseCases
from src.plan.application.dto.plan_request import PlanRequest
from src.plan.application.dto.plan_response import PlanResponse

router = APIRouter()

PlanUseCasesDependency = Annotated[PlanUseCases, Depends(get_plan_use_cases)]

@router.post('/plans', response_model=PlanResponse, tags=["plan"], status_code=HTTPStatus.CREATED)
async def create_plan(plan: PlanRequest, plan_use_cases: PlanUseCasesDependency):
    plan_validated = PlanRequest.model_validate(plan.model_dump())
    return plan_use_cases.create_plan(plan_validated)

@router.get('/plans', response_model=list[PlanResponse], tags=["plan"], status_code=HTTPStatus.OK)
async def get_plans(plan_use_cases: PlanUseCasesDependency):
    return plan_use_cases.get_plans()