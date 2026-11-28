import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlmodel import Session, create_engine, SQLModel

from src.core.dependencies import (
    get_engine,
    get_session,
    get_database_customer_repository,
    get_database_transaction_repository,
    get_database_plan_repository,
    get_customer_use_cases,
    get_transaction_use_cases,
    get_plan_use_cases,
    _in_memory_customer_repository,
    _in_memory_transaction_repository,
    _in_memory_plan_repository,
)
from src.customer.application.CustomerUseCases import CustomerUseCases
from src.customer.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from src.customer.infrastructure.repositories.sqlite_customer_repository import SqliteCustomerRepository
from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.transaction.infrastructure.repositories.in_memory_transaction_repository import InMemoryTransactionRepository
from src.transaction.infrastructure.repositories.sqlite_transaction_repository import SqliteTransactionRepository
from src.plan.application.PlanUseCases import PlanUseCases
from src.plan.infrastructure.repositories.in_memory_plan_repository import InMemoryPlanRepository
from src.plan.infrastructure.repositories.sqlite_plan_repository import SqlitePlanRepository


class TestGetEngine:

    @patch('src.core.dependencies.create_engine')
    @patch('src.core.dependencies.initialize_sqlite_schema')
    @patch('src.core.dependencies.config')
    def test_given_valid_config_when_get_engine_called_then_returns_engine(
        self, mock_config, mock_init_schema, mock_create_engine
    ):
        mock_config.DATABASE_NAME = 'test_db'
        mock_config.ENVIRONMENT = 'test'
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        engine = get_engine()
        
        assert engine is mock_engine
        mock_create_engine.assert_called_once()
        mock_init_schema.assert_called_once_with(mock_engine)

    @patch('src.core.dependencies.create_engine')
    @patch('src.core.dependencies.initialize_sqlite_schema')
    @patch('src.core.dependencies.config')
    def test_given_database_config_when_get_engine_called_then_uses_sqlite_url(
        self, mock_config, mock_init_schema, mock_create_engine
    ):
        mock_config.DATABASE_NAME = 'customer'
        mock_config.ENVIRONMENT = 'local'
        
        get_engine()
        
        call_args = mock_create_engine.call_args
        assert 'sqlite:///customer.local.sqlite3' in str(call_args)

    @patch('src.core.dependencies.create_engine')
    @patch('src.core.dependencies.initialize_sqlite_schema')
    @patch('src.core.dependencies.config')
    def test_given_get_engine_called_multiple_times_when_lru_cache_active_then_returns_same_instance(
        self, mock_config, mock_init_schema, mock_create_engine
    ):
        mock_config.DATABASE_NAME = 'test_db'
        mock_config.ENVIRONMENT = 'test'
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        engine1 = get_engine()
        engine2 = get_engine()
        
        assert engine1 is engine2
        mock_create_engine.assert_called_once()

    @pytest.fixture(autouse=True)
    def reset_engine_cache(self):
        get_engine.cache_clear()
        yield
        get_engine.cache_clear()


class TestGetSession:

    @patch('src.core.dependencies.get_engine')
    @patch('src.core.dependencies.config')
    def test_given_database_type_is_memory_when_get_session_called_then_yields_none(
        self, mock_config, mock_get_engine
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        
        session_generator = get_session()
        session = next(session_generator)
        
        assert session is None

    @patch('src.core.dependencies.Session')
    @patch('src.core.dependencies.get_engine')
    @patch('src.core.dependencies.config')
    def test_given_database_type_is_sqlite_when_get_session_called_then_yields_session(
        self, mock_config, mock_get_engine, mock_session_class
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine
        mock_session = Mock(spec=Session)
        mock_session_class.return_value.__enter__ = Mock(return_value=mock_session)
        mock_session_class.return_value.__exit__ = Mock(return_value=None)
        
        session_generator = get_session()
        session = next(session_generator)
        
        assert session is mock_session

    @patch('src.core.dependencies.Session')
    @patch('src.core.dependencies.get_engine')
    @patch('src.core.dependencies.config')
    def test_given_sqlite_session_when_get_session_exits_then_session_closed_properly(
        self, mock_config, mock_get_engine, mock_session_class
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine
        mock_session = Mock(spec=Session)
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_session)
        mock_context.__exit__ = Mock(return_value=None)
        mock_session_class.return_value = mock_context
        
        session_generator = get_session()
        next(session_generator)
        try:
            next(session_generator)
        except StopIteration:
            pass
        
        mock_context.__exit__.assert_called_once()


class TestInMemoryRepositories:

    def test_given_in_memory_customer_repository_when_called_then_returns_instance(self):
        repo = _in_memory_customer_repository()
        
        assert isinstance(repo, InMemoryCustomerRepository)

    def test_given_in_memory_customer_repository_when_called_multiple_times_then_returns_same_instance(self):
        repo1 = _in_memory_customer_repository()
        repo2 = _in_memory_customer_repository()
        
        assert repo1 is repo2

    def test_given_in_memory_transaction_repository_when_called_then_returns_instance(self):
        repo = _in_memory_transaction_repository()
        
        assert isinstance(repo, InMemoryTransactionRepository)

    def test_given_in_memory_transaction_repository_when_called_multiple_times_then_returns_same_instance(self):
        repo1 = _in_memory_transaction_repository()
        repo2 = _in_memory_transaction_repository()
        
        assert repo1 is repo2

    def test_given_in_memory_plan_repository_when_called_then_returns_instance(self):
        repo = _in_memory_plan_repository()
        
        assert isinstance(repo, InMemoryPlanRepository)

    def test_given_in_memory_plan_repository_when_called_multiple_times_then_returns_same_instance(self):
        repo1 = _in_memory_plan_repository()
        repo2 = _in_memory_plan_repository()
        
        assert repo1 is repo2


class TestGetDatabaseCustomerRepository:

    @patch('src.core.dependencies.config')
    def test_given_database_type_memory_when_get_customer_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        repo = get_database_customer_repository(mock_session)
        
        assert isinstance(repo, InMemoryCustomerRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_when_get_customer_repository_called_then_returns_sqlite_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        mock_session = Mock(spec=Session)
        
        repo = get_database_customer_repository(mock_session)
        
        assert isinstance(repo, SqliteCustomerRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_and_session_none_when_get_customer_repository_called_then_raises_error(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        
        with pytest.raises(RuntimeError, match='SQLite requires a database session'):
            get_database_customer_repository(None)

    @patch('src.core.dependencies.config')
    def test_given_database_type_unknown_when_get_customer_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'postgresql'
        mock_session = Mock(spec=Session)
        
        repo = get_database_customer_repository(mock_session)
        
        assert isinstance(repo, InMemoryCustomerRepository)


class TestGetDatabaseTransactionRepository:

    @patch('src.core.dependencies.config')
    def test_given_database_type_memory_when_get_transaction_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        repo = get_database_transaction_repository(mock_session)
        
        assert isinstance(repo, InMemoryTransactionRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_when_get_transaction_repository_called_then_returns_sqlite_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        mock_session = Mock(spec=Session)
        
        repo = get_database_transaction_repository(mock_session)
        
        assert isinstance(repo, SqliteTransactionRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_and_session_none_when_get_transaction_repository_called_then_raises_error(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        
        with pytest.raises(RuntimeError, match='SQLite requires a database session'):
            get_database_transaction_repository(None)

    @patch('src.core.dependencies.config')
    def test_given_database_type_unknown_when_get_transaction_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'unknown_type'
        mock_session = Mock(spec=Session)
        
        repo = get_database_transaction_repository(mock_session)
        
        assert isinstance(repo, InMemoryTransactionRepository)


class TestGetDatabasePlanRepository:

    @patch('src.core.dependencies.config')
    def test_given_database_type_memory_when_get_plan_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        repo = get_database_plan_repository(mock_session)
        
        assert isinstance(repo, InMemoryPlanRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_when_get_plan_repository_called_then_returns_sqlite_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        mock_session = Mock(spec=Session)
        
        repo = get_database_plan_repository(mock_session)
        
        assert isinstance(repo, SqlitePlanRepository)

    @patch('src.core.dependencies.config')
    def test_given_database_type_sqlite_and_session_none_when_get_plan_repository_called_then_raises_error(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        
        with pytest.raises(RuntimeError, match='SQLite requires a database session'):
            get_database_plan_repository(None)

    @patch('src.core.dependencies.config')
    def test_given_database_type_unknown_when_get_plan_repository_called_then_returns_in_memory_repo(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'unknown_type'
        mock_session = Mock(spec=Session)
        
        repo = get_database_plan_repository(mock_session)
        
        assert isinstance(repo, InMemoryPlanRepository)


class TestGetPlanUseCases:

    @patch('src.core.dependencies.config')
    def test_given_plan_repository_when_get_plan_use_cases_called_then_returns_plan_use_cases_instance(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        
        assert isinstance(use_cases, PlanUseCases)

    @patch('src.core.dependencies.config')
    def test_given_valid_repository_when_get_plan_use_cases_called_then_repository_injected_correctly(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        repo = get_database_plan_repository(mock_session)
        
        use_cases = get_plan_use_cases(repo)
        
        assert use_cases.plan_repository is repo


class TestGetCustomerUseCases:

    @patch('src.core.dependencies.config')
    def test_given_customer_repository_when_get_customer_use_cases_called_then_returns_customer_use_cases_instance(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        
        use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        assert isinstance(use_cases, CustomerUseCases)

    @patch('src.core.dependencies.config')
    def test_given_customer_repository_when_get_customer_use_cases_called_then_plan_lookup_adapter_injected(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        
        use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        assert use_cases.plan_lookup_port is not None

    @patch('src.core.dependencies.config')
    def test_given_customer_repository_when_get_customer_use_cases_called_then_repository_injected_correctly(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        
        use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        assert use_cases.customer_repository is customer_repo


class TestGetTransactionUseCases:

    @patch('src.core.dependencies.config')
    def test_given_transaction_repository_when_get_transaction_use_cases_called_then_returns_transaction_use_cases_instance(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        transaction_repo = get_database_transaction_repository(mock_session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        customer_use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        use_cases = get_transaction_use_cases(transaction_repo, customer_use_cases)
        
        assert isinstance(use_cases, TransactionUseCases)

    @patch('src.core.dependencies.config')
    def test_given_transaction_repository_when_get_transaction_use_cases_called_then_customer_lookup_adapter_injected(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        transaction_repo = get_database_transaction_repository(mock_session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        customer_use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        use_cases = get_transaction_use_cases(transaction_repo, customer_use_cases)
        
        assert use_cases.customer_lookup_port is not None

    @patch('src.core.dependencies.config')
    def test_given_transaction_repository_when_get_transaction_use_cases_called_then_repository_injected_correctly(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        transaction_repo = get_database_transaction_repository(mock_session)
        customer_repo = get_database_customer_repository(mock_session)
        plan_use_cases = get_plan_use_cases(get_database_plan_repository(mock_session))
        customer_use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        use_cases = get_transaction_use_cases(transaction_repo, customer_use_cases)
        
        assert use_cases.transaction_repository is transaction_repo


class TestDependencyInjectionIntegration:

    @patch('src.core.dependencies.config')
    def test_given_all_dependencies_when_full_dependency_tree_resolved_then_all_layers_connected(
        self, mock_config
    ):
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        mock_session = Mock(spec=Session)
        
        plan_repo = get_database_plan_repository(mock_session)
        plan_use_cases = get_plan_use_cases(plan_repo)
        
        customer_repo = get_database_customer_repository(mock_session)
        customer_use_cases = get_customer_use_cases(customer_repo, plan_use_cases)
        
        transaction_repo = get_database_transaction_repository(mock_session)
        transaction_use_cases = get_transaction_use_cases(transaction_repo, customer_use_cases)
        
        assert all([
            isinstance(plan_use_cases, PlanUseCases),
            isinstance(customer_use_cases, CustomerUseCases),
            isinstance(transaction_use_cases, TransactionUseCases),
        ])

    @patch('src.core.dependencies.config')
    def test_given_multiple_database_types_when_dependencies_resolved_then_correct_implementations_chosen(
        self, mock_config
    ):
        mock_session = Mock(spec=Session)
        
        mock_config.DEPENDENCY_DATABASE_TYPE = 'memory'
        memory_repo = get_database_customer_repository(mock_session)
        
        mock_config.DEPENDENCY_DATABASE_TYPE = 'sqlite'
        sqlite_repo = get_database_customer_repository(mock_session)
        
        assert isinstance(memory_repo, InMemoryCustomerRepository)
        assert isinstance(sqlite_repo, SqliteCustomerRepository)
        assert type(memory_repo) != type(sqlite_repo)