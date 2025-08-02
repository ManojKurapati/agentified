To write unit tests for the provided Python FastAPI code, we'll use `pytest` along with `unittest.mock` for mocking external dependencies like `Faker` and `random`.
We'll structure the tests in a `tests/` directory:
synthetic-data-generator/
├── app/
│   └── ... (existing code)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures for tests
│   └── unit/
│       ├── __init__.py
│       ├── test_config.py
│       ├── test_logging.py
│       ├── test_data_schema.py
│       ├── test_data_generator.py
│       └── test_api_endpoints.py
├── main.py
├── requirements.txt
└── ...
First, ensure you have `pytest` installed:
`pip install pytest`
---
### 1. `tests/conftest.py`
This file will contain shared fixtures, especially for mocking and setting up the FastAPI `TestClient`.
python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app as fastapi_app
from app.services.data_generator import SyntheticDataGenerator
from faker import Faker
import random
import datetime
@pytest.fixture(scope="module")
def client():
    """Provides a TestClient for the FastAPI application."""
    with TestClient(fastapi_app) as c:
        yield c
@pytest.fixture
def mock_faker():
    """Mocks the Faker instance used by SyntheticDataGenerator."""
    with patch('app.services.data_generator.Faker', autospec=True) as mock_faker_cls:
        mock_instance = MagicMock(spec=Faker)
        mock_faker_cls.return_value = mock_instance
        yield mock_instance
@pytest.fixture
def mock_random():
    """Mocks the random module."""
    with patch('app.services.data_generator.random', autospec=True) as mock_random_module:
        yield mock_random_module
@pytest.fixture
def data_generator_instance(mock_faker):
    """Provides an instance of SyntheticDataGenerator with a mocked Faker."""
    return SyntheticDataGenerator()
---
### 2. `tests/unit/test_config.py`
Tests for `app/core/config.py`.
python
# tests/unit/test_config.py
import os
import pytest
from app.core.config import Settings, settings
def test_settings_default_values():
    """Test that settings load with default values when env vars are not set."""
    # Temporarily clear relevant environment variables for this test
    original_app_name = os.environ.pop("APP_NAME", None)
    original_app_version = os.environ.pop("APP_VERSION", None)
    original_debug = os.environ.pop("DEBUG", None)
    try:
        # Re-instantiate Settings to pick up cleared env vars
        test_settings = Settings()
        assert test_settings.APP_NAME == "SyntheticDataGenerator"
        assert test_settings.APP_VERSION == "1.0.0"
        assert test_settings.DEBUG is False
    finally:
        # Restore original environment variables
        if original_app_name is not None:
            os.environ["APP_NAME"] = original_app_name
        if original_app_version is not None:
            os.environ["APP_VERSION"] = original_app_version
        if original_debug is not None:
            os.environ["DEBUG"] = original_debug
def test_settings_load_from_env_vars(monkeypatch):
    """Test that settings load correctly from environment variables."""
    monkeypatch.setenv("APP_NAME", "MyCustomApp")
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("DEBUG", "True")
    # Re-instantiate Settings to pick up mocked env vars
    test_settings = Settings()
    assert test_settings.APP_NAME == "MyCustomApp"
    assert test_settings.APP_VERSION == "2.0.0"
    assert test_settings.DEBUG is True
def test_settings_singleton_instance():
    """Test that the 'settings' object is a singleton and reflects env changes."""
    # This test confirms the global 'settings' object exists and is an instance of Settings.
    assert isinstance(settings, Settings)
---
### 3. `tests/unit/test_logging.py`
Tests for `app/core/logging.py`.
python
# tests/unit/test_logging.py
import logging
import sys
from unittest.mock import patch, MagicMock
import pytest
from app.core.logging import get_logger
from app.core.config import settings
@pytest.fixture(autouse=True)
def reset_logging_handlers():
    """Fixture to ensure a clean logging state for each test."""
    # Remove any existing handlers from the root logger and our specific logger
    # to prevent interference between tests.
    logging.getLogger().handlers = []
    # Clear specific logger from manager if it exists
    if 'test_logger' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger']
    if 'test_logger_debug' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_debug']
    if 'test_logger_info' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_info']
    if 'test_logger_handler' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_handler']
    if 'test_logger_stdout' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_stdout']
    if 'test_logger_formatter' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_formatter']
    if 'already_configured_logger' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['already_configured_logger']
    if 'fresh_logger_for_handler_test' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['fresh_logger_for_handler_test']
    yield
    # Clean up again after the test
    logging.getLogger().handlers = []
    # Repeat cleanup for specific loggers
    if 'test_logger' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger']
    if 'test_logger_debug' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_debug']
    if 'test_logger_info' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_info']
    if 'test_logger_handler' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_handler']
    if 'test_logger_stdout' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_stdout']
    if 'test_logger_formatter' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['test_logger_formatter']
    if 'already_configured_logger' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['already_configured_logger']
    if 'fresh_logger_for_handler_test' in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict['fresh_logger_for_handler_test']
def test_get_logger_returns_logger_instance():
    """Test that get_logger returns a logging.Logger instance."""
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
def test_get_logger_sets_level_debug_when_debug_true(monkeypatch):
    """Test logger level is DEBUG when settings.DEBUG is True."""
    monkeypatch.setattr(settings, "DEBUG", True)
    logger = get_logger("test_logger_debug")
    assert logger.level == logging.DEBUG
def test_get_logger_sets_level_info_when_debug_false(monkeypatch):
    """Test logger level is INFO when settings.DEBUG is False."""
    monkeypatch.setattr(settings, "DEBUG", False)
    logger = get_logger("test_logger_info")
    assert logger.level == logging.INFO
def test_get_logger_adds_console_handler_once():
    """Test that a StreamHandler is added to the logger and only once."""
    logger1 = get_logger("test_logger_handler")
    assert any(isinstance(h, logging.StreamHandler) for h in logger1.handlers)
    assert len(logger1.handlers) == 1 # Should only have one handler initially
    # Call again, should not add another handler
    logger2 = get_logger("test_logger_handler")
    assert len(logger2.handlers) == 1 # Still only one handler
def test_get_logger_handler_writes_to_stdout(capsys):
    """Test that the console handler writes to sys.stdout."""
    logger = get_logger("test_logger_stdout")
    logger.info("Test message for stdout.")
    captured = capsys.readouterr()
    assert "Test message for stdout." in captured.out
    assert not captured.err
def test_get_logger_formatter_is_set():
    """Test that the formatter is correctly set on the handler."""
    logger = get_logger("test_logger_formatter")
    handler = next((h for h in logger.handlers if isinstance(h, logging.StreamHandler)), None)
    assert handler is not None
    assert handler.formatter is not None
    # Check if the format string is part of the formatter's format
    assert "%(asctime)s - %(name)s - %(levelname)s - %(message)s" in handler.formatter._fmt
def test_get_logger_no_handlers_added_if_already_configured():
    """
    Test that get_logger does not add new handlers if the logger already has them.
    This is important for preventing duplicate log messages.
    """
    logger = logging.getLogger("already_configured_logger")
    logger.handlers = [] # Ensure clean state
    logger.addHandler(logging.NullHandler()) # Add a dummy handler
    initial_handlers_count = len(logger.handlers)
    # Call get_logger for the same logger name
    configured_logger = get_logger("already_configured_logger")
    # The number of handlers should not increase if get_logger's logic prevents duplicates
    assert len(configured_logger.handlers) == initial_handlers_count
    assert not any(isinstance(h, logging.StreamHandler) for h in configured_logger.handlers if h != logging.NullHandler())
    # Re-test the single handler addition with a fresh logger name to confirm the logic
    logger_fresh = get_logger("fresh_logger_for_handler_test")
    assert len(logger_fresh.handlers) == 1
    assert isinstance(logger_fresh.handlers[0], logging.StreamHandler)
---
### 4. `tests/unit/test_data_schema.py`
Tests for `app/models/data_schema.py`. This covers Pydantic model validation.
python
# tests/unit/test_data_schema.py
import pytest
from datetime import date, datetime
from pydantic import ValidationError
from app.models.data_schema import (
    GenerateRequest, GenerateResponse,
    StringField, IntegerField, FloatField, BooleanField,
    DateField, DateTimeField, EmailField, NameField, AddressField,
    UUIDField, PhoneNumberField, EnumField, ListField, ObjectField,
    FieldDefinition
)
# --- Test FieldDefinition Models ---
def test_string_field_valid():
    field = StringField(name="username", type="string", min_length=5, max_length=10, charset="alpha")
    assert field.name == "username"
    assert field.type == "string"
    assert field.min_length == 5
    assert field.max_length == 10
    assert field.charset == "alpha"
def test_string_field_defaults():
    field = StringField(name="description", type="string")
    assert field.min_length == 0
    assert field.max_length == 255
    assert field.charset == "alphanumeric"
def test_string_field_invalid_min_max_length():
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        StringField(name="test", type="string", min_length=-1)
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        StringField(name="test", type="string", max_length=0) # max_length must be PositiveInt
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        # This will fail because Pydantic validates types first, then constraints.
        # min_length=10, max_length=5 is caught by the PositiveInt/NonNegativeInt types,
        # not a direct min/max order check.
        StringField(name="test", type="string", min_length=10, max_length=5)
def test_integer_field_valid():
    field = IntegerField(name="age", type="integer", min_value=18, max_value=65)
    assert field.name == "age"
    assert field.type == "integer"
    assert field.min_value == 18
    assert field.max_value == 65
def test_integer_field_defaults():
    field = IntegerField(name="count", type="integer")
    assert field.min_value == 0
    assert field.max_value == 100
def test_float_field_valid():
    field = FloatField(name="price", type="float", min_value=10.0, max_value=100.0, decimal_places=2)
    assert field.name == "price"
    assert field.type == "float"
    assert field.min_value == 10.0
    assert field.max_value == 100.0
    assert field.decimal_places == 2
def test_float_field_defaults():
    field = FloatField(name="ratio", type="float")
    assert field.min_value == 0.0
    assert field.max_value == 100.0
    assert field.decimal_places == 2
def test_float_field_invalid_decimal_places():
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        FloatField(name="test", type="float", decimal_places=-1)
def test_boolean_field_valid():
    field = BooleanField(name="is_active", type="boolean")
    assert field.name == "is_active"
    assert field.type == "boolean"
def test_date_field_valid():
    field = DateField(name="birth_date", type="date", start_date="2000-01-01", end_date="2005-12-31")
    assert field.name == "birth_date"
    assert field.type == "date"
    assert field.start_date == date(2000, 1, 1)
    assert field.end_date == date(2005, 12, 31)
    assert field.date_format == "%Y-%m-%d"
def test_date_field_defaults():
    field = DateField(name="event_date", type="date")
    assert field.start_date == date(2000, 1, 1)
    assert field.end_date == date(2023, 12, 31)
def test_date_field_invalid_date_format():
    with pytest.raises(ValidationError, match="Input should be a valid date"):
        DateField(name="test", type="date", start_date="invalid-date")
def test_datetime_field_valid():
    field = DateTimeField(name="timestamp", type="datetime", start_datetime="2023-01-01T00:00:00", end_datetime="2023-01-01T23:59:59")
    assert field.name == "timestamp"
    assert field.type == "datetime"
    assert field.start_datetime == datetime(2023, 1, 1, 0, 0, 0)
    assert field.end_datetime == datetime(2023, 1, 1, 23, 59, 59)
    assert field.datetime_format == "%Y-%m-%dT%H:%M:%S"
def test_datetime_field_defaults():
    field = DateTimeField(name="log_time", type="datetime")
    assert field.start_datetime == datetime(2000, 1, 1, 0, 0, 0)
    assert field.end_datetime == datetime(2023, 12, 31, 23, 59, 59)
def test_email_field_valid():
    field = EmailField(name="user_email", type="email")
    assert field.name == "user_email"
    assert field.type == "email"
def test_name_field_valid():
    field = NameField(name="full_name", type="name")
    assert field.name == "full_name"
    assert field.type == "name"
def test_address_field_valid():
    field = AddressField(name="street_address", type="address")
    assert field.name == "street_address"
    assert field.type == "address"
def test_uuid_field_valid():
    field = UUIDField(name="record_id", type="uuid")
    assert field.name == "record_id"
    assert field.type == "uuid"
def test_phone_number_field_valid():
    field = PhoneNumberField(name="contact_number", type="phone_number")
    assert field.name == "contact_number"
    assert field.type == "phone_number"
def test_enum_field_valid():
    field = EnumField(name="status", type="enum", choices=["active", "inactive", "pending"])
    assert field.name == "status"
    assert field.type == "enum"
    assert field.choices == ["active", "inactive", "pending"]
def test_enum_field_empty_choices():
    with pytest.raises(ValidationError, match="List should have at least 1 item after validation, not 0"):
        EnumField(name="status", type="enum", choices=[])
def test_list_field_valid():
    item_def = StringField(name="tag", type="string")
    field = ListField(name="tags", type="list", item_definition=item_def, min_items=1, max_items=3)
    assert field.name == "tags"
    assert field.type == "list"
    assert isinstance(field.item_definition, StringField)
    assert field.min_items == 1
    assert field.max_items == 3
def test_list_field_defaults():
    item_def = IntegerField(name="number", type="integer")
    field = ListField(name="numbers", type="list", item_definition=item_def)
    assert field.min_items == 1
    assert field.max_items == 5
def test_list_field_invalid_min_max_items():
    item_def = StringField(name="tag", type="string")
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        ListField(name="test", type="list", item_definition=item_def, min_items=-1)
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        ListField(name="test", type="list", item_definition=item_def, max_items=0) # max_items must be PositiveInt
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        # This will fail because Pydantic validates types first, then constraints.
        ListField(name="test", type="list", item_definition=item_def, min_items=5, max_items=1)
def test_object_field_valid():
    nested_fields = [
        StringField(name="street", type="string"),
        IntegerField(name="zip", type="integer")
    ]
    field = ObjectField(name="address", type="object", fields=nested_fields)
    assert field.name == "address"
    assert field.type == "object"
    assert len(field.fields) == 2
    assert isinstance(field.fields[0], StringField)
    assert isinstance(field.fields[1], IntegerField)
def test_object_field_empty_fields():
    with pytest.raises(ValidationError, match="List should have at least 1 item after validation, not 0"):
        ObjectField(name="empty_obj", type="object", fields=[])
def test_field_definition_discriminator():
    """Test that FieldDefinition correctly discriminates between types."""
    schema_data = [
        {"name": "id", "type": "uuid"},
        {"name": "age", "type": "integer", "min_value": 10, "max_value": 20},
        {"name": "product_name", "type": "enum", "choices": ["A", "B"]},
        {
            "name": "address",
            "type": "object",
            "fields": [
                {"name": "street", "type": "string"},
                {"name": "city", "type": "string"}
            ]
        },
        {
            "name": "items",
            "type": "list",
            "item_definition": {"name": "item_id", "type": "uuid"}
        }
    ]
    parsed_schema = [FieldDefinition.model_validate(f) for f in schema_data]
    assert isinstance(parsed_schema[0], UUIDField)
    assert isinstance(parsed_schema[1], IntegerField)
    assert isinstance(parsed_schema[2], EnumField)
    assert isinstance(parsed_schema[3], ObjectField)
    assert isinstance(parsed_schema[4], ListField)
    assert isinstance(parsed_schema[3].fields[0], StringField)
    assert isinstance(parsed_schema[4].item_definition, UUIDField)
def test_field_definition_invalid_type():
    with pytest.raises(ValidationError, match="Discriminator 'type' has invalid value 'non_existent_type'"):
        FieldDefinition.model_validate({"name": "invalid", "type": "non_existent_type"})
# --- Test GenerateRequest and GenerateResponse Models ---
def test_generate_request_valid():
    request = GenerateRequest(
        num_records=5,
        schema=[
            StringField(name="name", type="string"),
            IntegerField(name="value", type="integer")
        ]
    )
    assert request.num_records == 5
    assert len(request.schema) == 2
    assert isinstance(request.schema[0], StringField)
def test_generate_request_invalid_num_records():
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        GenerateRequest(num_records=0, schema=[StringField(name="name", type="string")])
    with pytest.raises(ValidationError, match="Input should be less than or equal to 1000"):
        GenerateRequest(num_records=1001, schema=[StringField(name="name", type="string")])
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        GenerateRequest(num_records="abc", schema=[StringField(name="name", type="string")])
def test_generate_request_empty_schema():
    with pytest.raises(ValidationError, match="List should have at least 1 item after validation, not 0"):
        GenerateRequest(num_records=1, schema=[])
def test_generate_response_valid():
    data = [{"id": "123", "name": "Test"}, {"id": "456", "name": "Another"}]
    response = GenerateResponse(data=data)
    assert response.data == data
def test_generate_response_empty_data():
    response = GenerateResponse(data=[])
    assert response.data == []
def test_generate_response_invalid_data_type():
    with pytest.raises(ValidationError, match="Input should be a valid list"):
        GenerateResponse(data="not a list")
    with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
        GenerateResponse(data=[1, 2, 3]) # Should be list of dicts
---
### 5. `tests/unit/test_data_generator.py`
Tests for `app/services/data_generator.py`. This is the core logic for data generation.
python
# tests/unit/test_data_generator.py
import pytest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, call
from pydantic import ValidationError
from app.services.data_generator import SyntheticDataGenerator
from app.models.data_schema import (
    GenerateRequest,
    StringField, IntegerField, FloatField, BooleanField,
    DateField, DateTimeField, EmailField, NameField, AddressField,
    UUIDField, PhoneNumberField, EnumField, ListField, ObjectField
)
# Fixtures from conftest.py:
# - data_generator_instance (SyntheticDataGenerator with mocked Faker)
# - mock_faker
# - mock_random
class TestSyntheticDataGenerator:
    # --- Test _generate_value method for each field type ---
    def test_generate_value_string_field(self, data_generator_instance, mock_random):
        field_def = StringField(name="test_str", type="string", min_length=5, max_length=5, charset="abc")
        mock_random.randint.return_value = 5
        mock_random.choice.side_effect = ['a', 'b', 'c', 'a', 'b']
        result = data_generator_instance._generate_value(field_def)
        assert result == "abcab"
        mock_random.randint.assert_called_once_with(5, 5)
        assert mock_random.choice.call_count == 5
        mock_random.choice.assert_has_calls([call('abc')] * 5)
    def test_generate_value_string_field_default_charset(self, data_generator_instance, mock_random):
        field_def = StringField(name="test_str", type="string", min_length=3, max_length=3)
        mock_random.randint.return_value = 3
        mock_random.choice.side_effect = ['X', 'Y', 'Z'] # From alphanumeric
        result = data_generator_instance._generate_value(field_def)
        assert result == "XYZ"
        mock_random.randint.assert_called_once_with(3, 3)
        assert mock_random.choice.call_count == 3
        mock_random.choice.assert_has_calls([call("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")] * 3)
    def test_generate_value_integer_field(self, data_generator_instance, mock_random):
        field_def = IntegerField(name="test_int", type="integer", min_value=10, max_value=20)
        mock_random.randint.return_value = 15
        result = data_generator_instance._generate_value(field_def)
        assert result == 15
        mock_random.randint.assert_called_once_with(10, 20)
    def test_generate_value_float_field(self, data_generator_instance, mock_random):
        field_def = FloatField(name="test_float", type="float", min_value=1.0, max_value=10.0, decimal_places=2)
        mock_random.uniform.return_value = 5.6789
        result = data_generator_instance._generate_value(field_def)
        assert result == 5.68
        mock_random.uniform.assert_called_once_with(1.0, 10.0)
    def test_generate_value_boolean_field(self, data_generator_instance, mock_random):
        field_def = BooleanField(name="test_bool", type="boolean")
        mock_random.choice.side_effect = [True, False]
        assert data_generator_instance._generate_value(field_def) is True
        assert data_generator_instance._generate_value(field_def) is False
        assert mock_random.choice.call_count == 2
        mock_random.choice.assert_has_calls([call([True, False])] * 2)
    def test_generate_value_date_field(self, data_generator_instance, mock_random):
        start = date(2020, 1, 1)
        end = date(2020, 1, 3) # 2 days difference (0, 1, 2)
        field_def = DateField(name="test_date", type="date", start_date=start, end_date=end, date_format="%Y-%m-%d")
        mock_random.randint.return_value = 1 # 1 day after start_date
        result = data_generator_instance._generate_value(field_def)
        assert result == "2020-01-02"
        mock_random.randint.assert_called_once_with(0, (end - start).days)
    def test_generate_value_datetime_field(self, data_generator_instance, mock_random):
        start = datetime(2020, 1, 1, 0, 0, 0)
        end = datetime(2020, 1, 1, 0, 0, 10) # 10 seconds difference
        field_def = DateTimeField(name="test_dt", type="datetime", start_datetime=start, end_datetime=end, datetime_format="%H:%M:%S")
        mock_random.randint.return_value = 5 # 5 seconds after start_datetime
        result = data_generator_instance._generate_value(field_def)
        assert result == "00:00:05"
        mock_random.randint.assert_called_once_with(0, int((end - start).total_seconds()))
    def test_generate_value_email_field(self, data_generator_instance, mock_faker):
        field_def = EmailField(name="test_email", type="email")
        mock_faker.email.return_value = "test@example.com"
        result = data_generator_instance._generate_value(field_def)
        assert result == "test@example.com"
        mock_faker.email.assert_called_once()
    def test_generate_value_name_field(self, data_generator_instance, mock_faker):
        field_def = NameField(name="test_name", type="name")
        mock_faker.name.return_value = "John Doe"
        result = data_generator_instance._generate_value(field_def)
        assert result == "John Doe"
        mock_faker.name.assert_called_once()
    def test_generate_value_address_field(self, data_generator_instance, mock_faker):
        field_def = AddressField(name="test_address", type="address")
        mock_faker.address.return_value = "123 Main St"
        result = data_generator_instance._generate_value(field_def)
        assert result == "123 Main St"
        mock_faker.address.assert_called_once()
    def test_generate_value_uuid_field(self, data_generator_instance, mock_faker):
        field_def = UUIDField(name="test_uuid", type="uuid")
        mock_faker.uuid4.return_value = "a1b2c3d4-e5f6-7890-1234-567890abcdef"
        result = data_generator_instance._generate_value(field_def)
        assert result == "a1b2c3d4-e5f6-7890-1234-567890abcdef"
        mock_faker.uuid4.assert_called_once()
    def test_generate_value_phone_number_field(self, data_generator_instance, mock_faker):
        field_def = PhoneNumberField(name="test_phone", type="phone_number")
        mock_faker.phone_number.return_value = "1-555-555-1234"
        result = data_generator_instance._generate_value(field_def)
        assert result == "1-555-555-1234"
        mock_faker.phone_number.assert_called_once()
    def test_generate_value_enum_field(self, data_generator_instance, mock_random):
        choices = ["red", "green", "blue"]
        field_def = EnumField(name="test_enum", type="enum", choices=choices)
        mock_random.choice.return_value = "green"
        result = data_generator_instance._generate_value(field_def)
        assert result == "green"
        mock_random.choice.assert_called_once_with(choices)
    def test_generate_value_list_field(self, data_generator_instance, mock_random):
        item_def = IntegerField(name="item", type="integer", min_value=1, max_value=10)
        field_def = ListField(name="test_list", type="list", item_definition=item_def, min_items=2, max_items=2)
        mock_random.randint.side_effect = [2, 5, 8] # First for num_items, then for each item's value
        result = data_generator_instance._generate_value(field_def)
        assert result == [5, 8]
        mock_random.randint.assert_has_calls([call(2, 2), call(1, 10), call(1, 10)])
    def test_generate_value_object_field(self, data_generator_instance, mock_random, mock_faker):
        nested_fields = [
            StringField(name="street", type="string", min_length=5, max_length=5, charset="abc"),
            IntegerField(name="zip", type="integer", min_value=10000, max_value=99999)
        ]
        field_def = ObjectField(name="test_obj", type="object", fields=nested_fields)
        # Mock for street (string field)
        mock_random.randint.side_effect = [5, 12345] # for string length, then for zip
        mock_random.choice.side_effect = ['s', 't', 'r', 'e', 't']
        result = data_generator_instance._generate_value(field_def)
        assert result == {"street": "stret", "zip": 12345}
        # Verify calls for nested fields
        mock_random.randint.assert_any_call(5, 5) # For string length
        mock_random.choice.assert_has_calls([call("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")] * 5) # For string chars
        mock_random.randint.assert_any_call(10000, 99999) # For integer value
    def test_generate_value_unknown_field_type(self, data_generator_instance, caplog):
        # Create a mock field definition that doesn't match any known type
        # We use a simple MagicMock to avoid Pydantic validation on the mock itself
        mock_field_def = MagicMock()
        mock_field_def.name = "unknown"
        mock_field_def.type = "unknown_type"
        with caplog.at_level("WARNING"):
            result = data_generator_instance._generate_value(mock_field_def)
        assert result is None
        assert "Unknown field type encountered: unknown_type. Returning None." in caplog.text
    def test_generate_value_exception_handling(self, data_generator_instance, mock_random):
        # Mock a method to raise an exception
        mock_random.randint.side_effect = Exception("Mocked generation error")
        field_def = IntegerField(name="error_field", type="integer", min_value=1, max_value=10)
        with pytest.raises(ValueError, match="Failed to generate data for field 'error_field'"):
            data_generator_instance._generate_value(field_def)
    # --- Test generate_records method ---
    def test_generate_records_single_record_simple_schema(self, data_generator_instance, mock_faker, mock_random):
        schema = [
            UUIDField(name="id", type="uuid"),
            NameField(name="name", type="name"),
            IntegerField(name="age", type="integer", min_value=20, max_value=30)
        ]
        request = GenerateRequest(num_records=1, schema=schema)
        mock_faker.uuid4.return_value = "mock-uuid-1"
        mock_faker.name.return_value = "Mock Name 1"
        mock_random.randint.return_value = 25
        result = data_generator_instance.generate_records(request)
        assert len(result) == 1
        assert result[0] == {
            "id": "mock-uuid-1",
            "name": "Mock Name 1",
            "age": 25
        }
        mock_faker.uuid4.assert_called_once()
        mock_faker.name.assert_called_once()
        mock_random.randint.assert_called_once_with(20, 30)
    def test_generate_records_multiple_records_simple_schema(self, data_generator_instance, mock_faker, mock_random):
        schema = [
            EmailField(name="email", type="email"),
            BooleanField(name="is_active", type="boolean")
        ]
        request = GenerateRequest(num_records=3, schema=schema)
        mock_faker.email.side_effect = ["a@example.com", "b@example.com", "c@example.com"]
        mock_random.choice.side_effect = [True, False, True]
        result = data_generator_instance.generate_records(request)
        assert len(result) == 3
        assert result[0] == {"email": "a@example.com", "is_active": True}
        assert result[1] == {"email": "b@example.com", "is_active": False}
        assert result[2] == {"email": "c@example.com", "is_active": True}
        assert mock_faker.email.call_count == 3
        assert mock_random.choice.call_count == 3
    def test_generate_records_complex_nested_schema(self, data_generator_instance, mock_faker, mock_random):
        schema = [
            ObjectField(name="user", type="object", fields=[
                NameField(name="name", type="name"),
                EmailField(name="email", type="email")
            ]),
            ListField(name="tags", type="list", min_items=1, max_items=2, item_definition=EnumField(name="tag", type="enum", choices=["A", "B", "C"]))
        ]
        request = GenerateRequest(num_records=1, schema=schema)
        mock_faker.name.return_value = "Nested User"
        mock_faker.email.return_value = "nested@example.com"
        mock_random.randint.side_effect = [2] # For num_items in list
        mock_random.choice.side_effect = ["A", "C"] # For enum choices
        result = data_generator_instance.generate_records(request)
        assert len(result) == 1
        assert result[0] == {
            "user": {
                "name": "Nested User",
                "email": "nested@example.com"
            },
            "tags": ["A", "C"]
        }
        mock_faker.name.assert_called_once()
        mock_faker.email.assert_called_once()
        mock_random.randint.assert_called_once_with(1, 2)
        mock_random.choice.assert_has_calls([call(["A", "B", "C"]), call(["A", "B", "C"])])
    def test_generate_records_empty_schema_handled_by_pydantic(self, data_generator_instance):
        # Pydantic validation should prevent this from reaching generate_records
        with pytest.raises(ValidationError):
            GenerateRequest(num_records=1, schema=[])
    def test_generate_records_exception_propagation(self, data_generator_instance, mock_random):
        schema = [IntegerField(name="error_field", type="integer", min_value=1, max_value=10)]
        request = GenerateRequest(num_records=1, schema=schema)
        mock_random.randint.side_effect = Exception("Forced error during generation")
        with pytest.raises(ValueError, match="Failed to generate data for field 'error_field'"):
            data_generator_instance.generate_records(request)
    def test_generate_records_with_max_num_records(self, data_generator_instance, mock_faker):
        # Test with the maximum allowed number of records
        schema = [UUIDField(name="id", type="uuid")]
        request = GenerateRequest(num_records=1000, schema=schema)
        # Mock uuid4 to return distinct values for each call
        mock_faker.uuid4.side_effect = [f"uuid-{i}" for i in range(1000)]
        result = data_generator_instance.generate_records(request)
        assert len(result) == 1000
        assert mock_faker.uuid4.call_count == 1000
        assert result[0]["id"] == "uuid-0"
        assert result[999]["id"] == "uuid-999"
---
### 6. `tests/unit/test_api_endpoints.py`
Tests for `app/api/v1/endpoints/synthetic_data.py` using FastAPI's `TestClient`.
python
# tests/unit/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.models.data_schema import GenerateRequest, GenerateResponse
from app.services.data_generator import SyntheticDataGenerator
from app.main import app # Import the main FastAPI app instance
# Fixture from conftest.py: client (TestClient for app)
def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Synthetic Data Generator is running!"}
@patch('app.api.v1.endpoints.synthetic_data.SyntheticDataGenerator', autospec=True)
def test_generate_synthetic_data_success(mock_generator_cls, client):
    """Test successful data generation via the API endpoint."""
    mock_generator_instance = mock_generator_cls.return_value
    # Mock the generate_records method to return predictable data
    mock_generated_data = [
        {"id": "uuid-1", "name": "Test User 1"},
        {"id": "uuid-2", "name": "Test User 2"}
    ]
    mock_generator_instance.generate_records.return_value = mock_generated_data
    request_payload = {
        "num_records": 2,
        "schema": [
            {"name": "id", "type": "uuid"},
            {"name": "name", "type": "name"}
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 200
    assert response.json() == {"data": mock_generated_data}
    # Verify that the generator's method was called with the correct request object
    mock_generator_instance.generate_records.assert_called_once()
    called_request = mock_generator_instance.generate_records.call_args[0][0]
    assert isinstance(called_request, GenerateRequest)
    assert called_request.num_records == 2
    assert called_request.schema[0].name == "id"
    assert called_request.schema[1].name == "name"
@patch('app.api.v1.endpoints.synthetic_data.SyntheticDataGenerator', autospec=True)
def test_generate_synthetic_data_validation_error_num_records(mock_generator_cls, client):
    """Test API handles Pydantic validation errors for num_records."""
    request_payload = {
        "num_records": 0,  # Invalid: must be positive
        "schema": [
            {"name": "id", "type": "uuid"}
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)
    assert "value must be greater than 0" in response.json()["detail"][0]["msg"]
    mock_generator_cls.return_value.generate_records.assert_not_called()
@patch('app.api.v1.endpoints.synthetic_data.SyntheticDataGenerator', autospec=True)
def test_generate_synthetic_data_validation_error_empty_schema(mock_generator_cls, client):
    """Test API handles Pydantic validation errors for empty schema."""
    request_payload = {
        "num_records": 1,
        "schema": []  # Invalid: min_length=1
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 422
    assert "List should have at least 1 item after validation, not 0" in response.json()["detail"][0]["msg"]
    mock_generator_cls.return_value.generate_records.assert_not_called()
@patch('app.api.v1.endpoints.synthetic_data.SyntheticDataGenerator', autospec=True)
def test_generate_synthetic_data_validation_error_invalid_field_type(mock_generator_cls, client):
    """Test API handles Pydantic validation errors for invalid field types in schema."""
    request_payload = {
        "num_records": 1,
        "schema": [
            {"name": "id", "type": "invalid_type"}  # Invalid type
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 422
    assert "Discriminator 'type' has invalid value 'invalid_type'" in response.json()["detail"][0]["msg"]
    mock_generator_cls.return_value.generate_records.assert_not_called()
@patch('app.api.v1.endpoints.synthetic_data.SyntheticDataGenerator', autospec=True)
def test_generate_synthetic_data_internal_server_error(mock_generator_cls, client):
    """Test API handles internal exceptions during data generation."""
    mock_generator_instance = mock_generator_cls.return_value
    # Mock generate_records to raise an arbitrary exception
    mock_generator_instance.generate_records.side_effect = Exception("Simulated internal error")
    request_payload = {
        "num_records": 1,
        "schema": [
            {"name": "id", "type": "uuid"}
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate synthetic data: Simulated internal error"
    mock_generator_instance.generate_records.assert_called_once()
def test_generate_synthetic_data_max_records_limit(client):
    """Test that num_records exceeding 1000 results in a validation error."""
    request_payload = {
        "num_records": 1001,
        "schema": [
            {"name": "id", "type": "uuid"}
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 422
    assert "value must be less than or equal to 1000" in response.json()["detail"][0]["msg"]
def test_generate_synthetic_data_min_records_limit(client):
    """Test that num_records of 1 is valid."""
    request_payload = {
        "num_records": 1,
        "schema": [
            {"name": "id", "type": "uuid"}
        ]
    }
    # We don't mock the generator here, as we want to test the full API path for a valid request.
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 200 # Should pass validation
    assert "data" in response.json()
    assert len(response.json()["data"]) == 1
    assert "id" in response.json()["data"][0] # Check for the generated field
def test_generate_synthetic_data_complex_schema_validation(client):
    """Test validation with a complex nested schema, ensuring Pydantic handles it."""
    request_payload = {
        "num_records": 1,
        "schema": [
            {
                "name": "order_id",
                "type": "uuid"
            },
            {
                "name": "customer_info",
                "type": "object",
                "fields": [
                    {
                        "name": "customer_name",
                        "type": "name"
                    },
                    {
                        "name": "customer_email",
                        "type": "email"
                    }
                ]
            },
            {
                "name": "items",
                "type": "list",
                "min_items": 1,
                "max_items": 3,
                "item_definition": {
                    "name": "item",
                    "type": "object",
                    "fields": [
                        {
                            "name": "product_name",
                            "type": "enum",
                            "choices": ["Laptop", "Mouse", "Keyboard", "Monitor"]
                        },
                        {
                            "name": "quantity",
                            "type": "integer",
                            "min_value": 1,
                            "max_value": 5
                        },
                        {
                            "name": "price_usd",
                            "type": "float",
                            "min_value": 10.0,
                            "max_value": 1000.0,
                            "decimal_places": 2
                        }
                    ]
                }
            },
            {
                "name": "order_date",
                "type": "datetime",
                "start_datetime": "2023-01-01T00:00:00",
                "end_datetime": "2023-12-31T23:59:59",
                "datetime_format": "%Y-%m-%d %H:%M:%S"
            }
        ]
    }
    response = client.post("/api/v1/generate", json=request_payload)
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 1
    # Basic check for structure of generated data
    record = response.json()["data"][0]
    assert "order_id" in record
    assert "customer_info" in record
    assert "items" in record
    assert "order_date" in record
    assert isinstance(record["customer_info"], dict)
    assert isinstance(record["items"], list)
    assert len(record["items"]) >= 1 and len(record["items"]) <= 3
    if record["items"]:
        assert isinstance(record["items"][0], dict)
        assert "product_name" in record["items"][0]
        assert "quantity" in record["items"][0]
        assert "price_usd" in record["items"][0]
---
### How to Run the Tests
1.  Save the test files in the `tests/unit/` directory as shown in the structure.
2.  Make sure your `requirements.txt` includes `pytest`, `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `python-dotenv`, and `Faker`.
3.  Navigate to the root of your project (`synthetic-data-generator/`) in your terminal.
4.  Run pytest:
    ```bash
    pytest
This comprehensive set of unit tests covers the core logic, data models, and API endpoints, including various edge cases and error handling, ensuring the robustness and correctness of your FastAPI backend.