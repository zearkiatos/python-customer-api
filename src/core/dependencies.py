import os
from functools import lru_cache
from typing import Annotated, Iterator
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.domain.repositories.customer_repository import CustomerRepository
from src.customer.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from src.customer.infrastructure.repositories.sqlite_customer_repository import SqliteCustomerRepository
from src.core.config import Config
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
    SQLModel.metadata.create_all(engine)
    return engine

def get_session() -> Iterator[Session]:
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
        return _sqlite_transaction_repository(session)
    else:
        return _in_memory_transaction_repository()

def get_customer_use_cases(
    repository: Annotated[CustomerRepository, Depends(get_database_customer_repository)],
) -> CustomerUseCases:
    return CustomerUseCases(None, repository)

def get_transaction_use_cases(
    repository: Annotated[TransactionRepository, Depends(get_database_transaction_repository)],
    customer_use_cases: Annotated[
        CustomerUseCases,
        Depends(get_customer_use_cases),
    ],
) -> TransactionUseCases:
    adapter = CustomerLookupAdapter(customer_use_cases)
    return TransactionUseCases(None, repository, customer_lookup_port=adapter)