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

config = Config()

@lru_cache
def get_engine():
    url = config.DATABASE_URL
    engine = create_engine(url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine

def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session

@lru_cache
def _in_memory_repository() -> InMemoryCustomerRepository:
    return InMemoryCustomerRepository()

def get_database_repository(
    session: Annotated[Session, Depends(get_session)],
) -> CustomerRepository:
    database_type = config.DEPENDENCY_DATABASE_TYPE
    if database_type == "memory":
        return _in_memory_repository()
    if database_type == "sqlite":
        return SqliteCustomerRepository(session)
    else:
        return _in_memory_repository()

def get_customer_use_cases(
    repository: Annotated[CustomerRepository, Depends(get_database_repository)],
) -> CustomerUseCases:
    return CustomerUseCases(None, repository)