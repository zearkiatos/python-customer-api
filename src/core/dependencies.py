import os
from functools import lru_cache
from typing import Annotated, Iterator
from fastapi import Depends
from sqlmodel import Session, create_engine
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.domain.repositories.customer_repository import CustomerRepository
from src.customer.infrastructure.adapters.plan_lookup_adapter import PlanLookupAdapter
from src.customer.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from src.customer.infrastructure.repositories.sqlite_customer_repository import SqliteCustomerRepository
from src.core.config import Config
from src.core.sqlite_schema import initialize_sqlite_schema
from src.plan.application.PlanUseCases import PlanUseCases
from src.plan.domain.repositories.plan_repository import PlanRepository
from src.plan.infrastructure.repositories.in_memory_plan_repository import InMemoryPlanRepository
from src.plan.infrastructure.repositories.sqlite_plan_repository import SqlitePlanRepository
from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.transaction.domain.repositories.transaction_repository import TransactionRepository
from src.transaction.infrastructure.adapters.customer_lookup_adapter import CustomerLookupAdapter
from src.transaction.infrastructure.repositories.in_memory_transaction_repository import InMemoryTransactionRepository
from src.transaction.infrastructure.repositories.sqlite_transaction_repository import SqliteTransactionRepository

config = Config()

@lru_cache
def get_engine():
    url = f"sqlite:///{config.DATABASE_NAME}.{config.ENVIRONMENT}.sqlite3"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    initialize_sqlite_schema(engine)
    return engine

def get_session() -> Iterator[Session | None]:
    if config.DEPENDENCY_DATABASE_TYPE != "sqlite":
        yield None
        return
    
    with Session(get_engine()) as session:
        yield session

@lru_cache
def _in_memory_customer_repository() -> InMemoryCustomerRepository:
    return InMemoryCustomerRepository()

def _sqlite_customer_repository(session: Session) -> SqliteCustomerRepository:
    return SqliteCustomerRepository(session)

def get_database_customer_repository(
    session: Annotated[Session, Depends(get_session)],
) -> CustomerRepository:
    database_type = config.DEPENDENCY_DATABASE_TYPE
    if database_type == "memory":
        return _in_memory_customer_repository()
    if database_type == "sqlite":
        if session is None:
            raise RuntimeError("SQLite requires a database session")
        return _sqlite_customer_repository(session)
    else:
        return _in_memory_customer_repository()

@lru_cache
def _in_memory_transaction_repository() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()

def _sqlite_transaction_repository(session: Session) -> SqliteTransactionRepository:
    return SqliteTransactionRepository(session)

def get_database_transaction_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TransactionRepository:
    database_type = config.DEPENDENCY_DATABASE_TYPE
    if database_type == "memory":
        return _in_memory_transaction_repository()
    if database_type == "sqlite":
        if session is None:
            raise RuntimeError("SQLite requires a database session")
        return _sqlite_transaction_repository(session)
    else:
        return _in_memory_transaction_repository()


@lru_cache
def _in_memory_plan_repository() -> InMemoryPlanRepository:
    return InMemoryPlanRepository()

def _sqlite_plan_repository(session: Session) -> SqlitePlanRepository:
    return SqlitePlanRepository(session)

def get_database_plan_repository(
    session: Annotated[Session, Depends(get_session)],
) -> PlanRepository:
    database_type = config.DEPENDENCY_DATABASE_TYPE
    if database_type == "memory":
        return _in_memory_plan_repository()
    if database_type == "sqlite":
        if session is None:
            raise RuntimeError("SQLite requires a database session")
        return _sqlite_plan_repository(session)
    else:
        return _in_memory_plan_repository()

def get_plan_use_cases(
    repository: Annotated[PlanRepository, Depends(get_database_plan_repository)],
) -> PlanUseCases:
    return PlanUseCases(repository)

def get_plan_use_cases(
    repository: Annotated[PlanRepository, Depends(get_database_plan_repository)],
) -> PlanUseCases:
    return PlanUseCases(repository)

def get_customer_use_cases(
    repository: Annotated[CustomerRepository, Depends(get_database_customer_repository)],
    plan_use_cases: Annotated[PlanUseCases, Depends(get_plan_use_cases)],
) -> CustomerUseCases:
    adapter = PlanLookupAdapter(plan_use_cases)
    return CustomerUseCases(None, repository, plan_lookup_port=adapter)

def get_transaction_use_cases(
    repository: Annotated[TransactionRepository, Depends(get_database_transaction_repository)],
    customer_use_cases: Annotated[
        CustomerUseCases,
        Depends(get_customer_use_cases),
    ],
) -> TransactionUseCases:
    adapter = CustomerLookupAdapter(customer_use_cases)
    return TransactionUseCases(None, repository, customer_lookup_port=adapter)