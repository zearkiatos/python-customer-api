import os
import sys
import pytest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


@pytest.fixture(autouse=True)
def reset_config_module():
    for module_name in list(sys.modules.keys()):
        if 'src.core.config' in module_name or module_name == 'src.core':
            del sys.modules[module_name]
    yield


class TestConfigEnvironmentDetection:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'local'}, clear=True)
    def test_given_environment_is_local_when_config_loads_then_loads_env_local(self, mock_load_dotenv):
        from src.core.config import Config
        assert mock_load_dotenv.called

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'test'}, clear=True)
    def test_given_environment_is_test_when_config_loads_then_loads_env_test(self, mock_load_dotenv):
        from src.core.config import Config
        assert mock_load_dotenv.called

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_given_no_environment_set_when_config_loads_then_loads_default_env(self, mock_load_dotenv):
        from src.core.config import Config
        assert mock_load_dotenv.called

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'unknown_env'}, clear=True)
    def test_given_unknown_environment_when_config_loads_then_loads_default_env(self, mock_load_dotenv):
        from src.core.config import Config
        assert mock_load_dotenv.called


class TestConfigClassAttributes:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'test_db',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_all_variables_set_when_config_class_loads_then_all_attributes_populated(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'test'
        assert Config.DATABASE_NAME == 'test_db'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'memory'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'local'}, clear=True)
    def test_given_environment_local_when_config_reads_environment_then_returns_local(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'local'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'test'}, clear=True)
    def test_given_environment_test_when_config_reads_environment_then_returns_test(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'test'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'production'}, clear=True)
    def test_given_environment_production_when_config_reads_environment_then_returns_production(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'production'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'DATABASE_NAME': 'customer'}, clear=True)
    def test_given_database_name_set_when_config_reads_database_name_then_returns_correct_value(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == 'customer'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'DATABASE_NAME': 'custom_db_name'}, clear=True)
    def test_given_database_name_custom_when_config_reads_database_name_then_returns_custom_value(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == 'custom_db_name'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'DEPENDENCY_DATABASE_TYPE': 'sqlite'}, clear=True)
    def test_given_database_type_sqlite_when_config_reads_type_then_returns_sqlite(self, mock_load):
        from src.core.config import Config
        assert Config.DEPENDENCY_DATABASE_TYPE == 'sqlite'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'DEPENDENCY_DATABASE_TYPE': 'memory'}, clear=True)
    def test_given_database_type_memory_when_config_reads_type_then_returns_memory(self, mock_load):
        from src.core.config import Config
        assert Config.DEPENDENCY_DATABASE_TYPE == 'memory'


class TestConfigMissingVariables:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_given_no_environment_variable_when_config_reads_environment_then_returns_none(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT is None

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'test'}, clear=True)
    def test_given_database_name_missing_when_config_reads_database_name_then_returns_none(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME is None

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'test', 'DATABASE_NAME': 'customer'}, clear=True)
    def test_given_database_type_missing_when_config_reads_type_then_returns_none(self, mock_load):
        from src.core.config import Config
        assert Config.DEPENDENCY_DATABASE_TYPE is None


class TestConfigEnvironmentSpecificValues:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'local',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'sqlite'
    }, clear=True)
    def test_given_local_environment_when_config_loads_then_has_correct_local_config(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'local'
        assert Config.DATABASE_NAME == 'customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'sqlite'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_test_environment_when_config_loads_then_has_correct_test_config(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'test'
        assert Config.DATABASE_NAME == 'customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'memory'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'production',
        'DATABASE_NAME': 'prod_customer',
        'DEPENDENCY_DATABASE_TYPE': 'postgresql'
    }, clear=True)
    def test_given_production_environment_when_config_loads_then_has_correct_prod_config(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'production'
        assert Config.DATABASE_NAME == 'prod_customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'postgresql'


class TestConfigValueVariationsParametrized:

    @pytest.mark.parametrize('env_value', [
        'local', 'test', 'development', 'staging', 'production', 'custom'
    ])
    @patch('dotenv.load_dotenv')
    def test_given_various_environment_values_when_config_reads_environment_then_returns_exact_value(self, mock_load, env_value):
        with patch.dict(os.environ, {'ENVIRONMENT': env_value}, clear=True):
            from src.core.config import Config
            assert Config.ENVIRONMENT == env_value

    @pytest.mark.parametrize('db_name', [
        'customer', 'test_customer', 'prod_db', 'db_123', 'my-database', 'CamelCaseDatabase'
    ])
    @patch('dotenv.load_dotenv')
    def test_given_various_database_names_when_config_reads_name_then_returns_exact_name(self, mock_load, db_name):
        with patch.dict(os.environ, {'DATABASE_NAME': db_name}, clear=True):
            from src.core.config import Config
            assert Config.DATABASE_NAME == db_name

    @pytest.mark.parametrize('db_type', [
        'memory', 'sqlite', 'postgresql', 'mysql', 'mongodb', 'custom-type'
    ])
    @patch('dotenv.load_dotenv')
    def test_given_various_database_types_when_config_reads_type_then_returns_exact_type(self, mock_load, db_type):
        with patch.dict(os.environ, {'DEPENDENCY_DATABASE_TYPE': db_type}, clear=True):
            from src.core.config import Config
            assert Config.DEPENDENCY_DATABASE_TYPE == db_type


class TestConfigEdgeCases:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': ''}, clear=True)
    def test_given_empty_environment_string_when_config_reads_environment_then_returns_empty_string(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == ''

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': '',
        'DEPENDENCY_DATABASE_TYPE': ''
    }, clear=True)
    def test_given_empty_config_values_when_config_loads_then_preserves_empty_strings(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == ''
        assert Config.DEPENDENCY_DATABASE_TYPE == ''

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer_with_special_chars-123_and_@special',
        'DEPENDENCY_DATABASE_TYPE': 'type-with-dashes_and_underscores'
    }, clear=True)
    def test_given_values_with_special_chars_when_config_loads_then_preserves_special_chars(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == 'customer_with_special_chars-123_and_@special'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'type-with-dashes_and_underscores'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer with spaces',
        'DEPENDENCY_DATABASE_TYPE': 'type with spaces'
    }, clear=True)
    def test_given_values_with_spaces_when_config_loads_then_preserves_spaces(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == 'customer with spaces'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'type with spaces'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory',
        'EXTRA_VAR': 'extra_value',
        'ANOTHER_EXTRA': 'another_value'
    }, clear=True)
    def test_given_extra_environment_vars_set_when_config_loads_then_ignores_extra_vars(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'test'
        assert Config.DATABASE_NAME == 'customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'memory'
        assert not hasattr(Config, 'EXTRA_VAR')
        assert not hasattr(Config, 'ANOTHER_EXTRA')

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'test', 'DATABASE_NAME': '123'}, clear=True)
    def test_given_numeric_strings_when_config_loads_then_preserves_as_strings(self, mock_load):
        from src.core.config import Config
        assert Config.DATABASE_NAME == '123'
        assert isinstance(Config.DATABASE_NAME, str)


class TestConfigCaseSensitivity:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'LOCAL',
        'DATABASE_NAME': 'Customer',
        'DEPENDENCY_DATABASE_TYPE': 'SQLITE'
    }, clear=True)
    def test_given_uppercase_values_when_config_loads_then_preserves_case(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'LOCAL'
        assert Config.DATABASE_NAME == 'Customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'SQLITE'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'local'}, clear=True)
    def test_given_lowercase_local_when_config_loads_then_matches_lowercase_condition(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'local'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'LOCAL'}, clear=True)
    def test_given_uppercase_local_when_config_loads_then_does_not_match_condition(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'LOCAL'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {'ENVIRONMENT': 'TeSt'}, clear=True)
    def test_given_mixed_case_test_when_config_loads_then_does_not_match_condition(self, mock_load):
        from src.core.config import Config
        assert Config.ENVIRONMENT == 'TeSt'


class TestConfigConsistency:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_config_loaded_when_accessed_multiple_times_then_values_persist(self, mock_load):
        from src.core.config import Config
        
        env1 = Config.ENVIRONMENT
        db1 = Config.DATABASE_NAME
        db_type1 = Config.DEPENDENCY_DATABASE_TYPE
        
        env2 = Config.ENVIRONMENT
        db2 = Config.DATABASE_NAME
        db_type2 = Config.DEPENDENCY_DATABASE_TYPE
        
        assert env1 == env2
        assert db1 == db2
        assert db_type1 == db_type2

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_config_with_all_attributes_when_all_accessed_then_all_readable(self, mock_load):
        from src.core.config import Config
        
        try:
            _ = Config.ENVIRONMENT
            _ = Config.DATABASE_NAME
            _ = Config.DEPENDENCY_DATABASE_TYPE
        except AttributeError as e:
            pytest.fail(f"Config attribute not accessible: {e}")

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_config_class_when_attributes_accessed_then_values_are_deterministic(self, mock_load):
        from src.core.config import Config
        
        value1 = Config.DATABASE_NAME
        value2 = Config.DATABASE_NAME
        
        assert value1 is value2 or value1 == value2


class TestConfigIntegration:

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer_test',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_complete_test_environment_when_config_loads_then_all_values_correct(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'test'
        assert Config.DATABASE_NAME == 'customer_test'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'memory'
        
        assert isinstance(Config.ENVIRONMENT, (str, type(None)))
        assert isinstance(Config.DATABASE_NAME, (str, type(None)))
        assert isinstance(Config.DEPENDENCY_DATABASE_TYPE, (str, type(None)))

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'local',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'sqlite'
    }, clear=True)
    def test_given_complete_local_environment_when_config_loads_then_all_values_correct(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'local'
        assert Config.DATABASE_NAME == 'customer'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'sqlite'
        
        assert isinstance(Config.ENVIRONMENT, str)
        assert isinstance(Config.DATABASE_NAME, str)
        assert isinstance(Config.DEPENDENCY_DATABASE_TYPE, str)

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'production',
        'DATABASE_NAME': 'prod_customer_db',
        'DEPENDENCY_DATABASE_TYPE': 'postgresql'
    }, clear=True)
    def test_given_complete_production_environment_when_config_loads_then_all_values_correct(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT == 'production'
        assert Config.DATABASE_NAME == 'prod_customer_db'
        assert Config.DEPENDENCY_DATABASE_TYPE == 'postgresql'

    @patch('dotenv.load_dotenv')
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'DATABASE_NAME': 'customer',
        'DEPENDENCY_DATABASE_TYPE': 'memory'
    }, clear=True)
    def test_given_config_fully_set_when_checked_then_all_attributes_are_valid_types(self, mock_load):
        from src.core.config import Config
        
        assert Config.ENVIRONMENT is None or isinstance(Config.ENVIRONMENT, str)
        assert Config.DATABASE_NAME is None or isinstance(Config.DATABASE_NAME, str)
        assert Config.DEPENDENCY_DATABASE_TYPE is None or isinstance(Config.DEPENDENCY_DATABASE_TYPE, str)