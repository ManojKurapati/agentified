The product requirement is concise: "nocode tool to generate synthetic data." This implies a need for an API where users can define the *structure* of the data they want, and the backend generates it without requiring code.
Here's a FastAPI backend implementation that addresses this, focusing on clean route definitions, robust request validation using Pydantic, and adherence to best practices.
---
## FastAPI Backend for Synthetic Data Generation
This application provides a simple API to generate structured synthetic data based on a user-defined schema.
### Project Structure
synthetic-data-generator/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   └── synthetic_data.py
│   │   │   └── router.py
│   │   └── router.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_schema.py
│   └── services/
│       ├── __init__.py
│       └── data_generator.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
### Setup Instructions
1.  **Clone the repository (or create the files manually):**
    ```bash
    mkdir synthetic-data-generator
    cd synthetic-data-generator
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    (Or manually: `pip install fastapi uvicorn pydantic python-dotenv faker`)
4.  **Create a `.env` file** (based on `.env.example`):
    # .env
    APP_NAME="Synthetic Data Generator"
    APP_VERSION="1.0.0"
    DEBUG=True
5.  **Run the application:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    The API will be available at `http://localhost:8000`.
    The interactive API documentation (Swagger UI) will be at `http://localhost:8000/docs`.
    The alternative API documentation (ReDoc) will be at `http://localhost:8000/redoc`.
---
### Code Implementation
#### `requirements.txt`
fastapi==0.111.0
uvicorn==0.30.1
pydantic==2.7.4
pydantic-settings==2.3.3
python-dotenv==1.0.1
Faker==25.8.0
#### `main.py`
python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import get_logger
logger = get_logger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application startup and shutdown events.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")
    # Any startup logic can go here (e.g., database connections, cache warm-up)
    yield
    # Any shutdown logic can go here (e.g., closing database connections)
    logger.info(f"Shutting down {settings.APP_NAME}...")
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A nocode tool to generate synthetic data.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)
# Configure CORS middleware
# Adjust `allow_origins` in a production environment to only include your frontend domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Include the API router
app.include_router(api_router, prefix="/api")
@app.get("/health", summary="Health Check")
async def health_check():
    """
    Endpoint to check the health of the API.
    Returns a simple status message.
    """
    logger.info("Health check requested.")
    return {"status": "ok", "message": f"{settings.APP_NAME} is running!"}
#### `app/core/config.py`
python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    APP_NAME: str = Field("SyntheticDataGenerator", description="Name of the application")
    APP_VERSION: str = Field("1.0.0", description="Version of the application")
    DEBUG: bool = Field(False, description="Enable debug mode (e.g., for detailed logging)")
settings = Settings()
#### `app/core/logging.py`
python
# app/core/logging.py
import logging
import sys
from app.core.config import settings
def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    # Prevent adding multiple handlers if the logger is already configured
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
#### `app/models/data_schema.py`
python
# app/models/data_schema.py
from typing import List, Dict, Any, Union, Literal
from datetime import date, datetime
from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt
from typing_extensions import Annotated # For Python < 3.9, use typing.Union and then Annotated
# --- Base Field Definition ---
class BaseFieldDefinition(BaseModel):
    """
    Base model for all field definitions.
    Uses a 'type' discriminator for polymorphic validation.
    """
    name: str = Field(..., description="The name of the field (e.g., 'first_name', 'age').")
    type: str = Field(..., description="The type of data to generate for this field.")
# --- Specific Field Types ---
class StringField(BaseFieldDefinition):
    type: Literal["string"] = "string"
    min_length: NonNegativeInt = Field(0, description="Minimum length of the generated string.")
    max_length: PositiveInt = Field(255, description="Maximum length of the generated string.")
    charset: str = Field("alphanumeric", description="Character set for string generation. 'alphanumeric', 'alpha', 'numeric', or custom string.")
class IntegerField(BaseFieldDefinition):
    type: Literal["integer"] = "integer"
    min_value: int = Field(0, description="Minimum value for the generated integer.")
    max_value: int = Field(100, description="Maximum value for the generated integer.")
class FloatField(BaseFieldDefinition):
    type: Literal["float"] = "float"
    min_value: float = Field(0.0, description="Minimum value for the generated float.")
    max_value: float = Field(100.0, description="Maximum value for the generated float.")
    decimal_places: NonNegativeInt = Field(2, description="Number of decimal places for the generated float.")
class BooleanField(BaseFieldDefinition):
    type: Literal["boolean"] = "boolean"
class DateField(BaseFieldDefinition):
    type: Literal["date"] = "date"
    start_date: date = Field(date(2000, 1, 1), description="Start date for generation (YYYY-MM-DD).")
    end_date: date = Field(date(2023, 12, 31), description="End date for generation (YYYY-MM-DD).")
    date_format: str = Field("%Y-%m-%d", description="Format for the generated date (e.g., '%Y-%m-%d').")
class DateTimeField(BaseFieldDefinition):
    type: Literal["datetime"] = "datetime"
    start_datetime: datetime = Field(datetime(2000, 1, 1, 0, 0, 0), description="Start datetime for generation (YYYY-MM-DDTHH:MM:SS).")
    end_datetime: datetime = Field(datetime(2023, 12, 31, 23, 59, 59), description="End datetime for generation (YYYY-MM-DDTHH:MM:SS).")
    datetime_format: str = Field("%Y-%m-%dT%H:%M:%S", description="Format for the generated datetime (e.g., '%Y-%m-%dT%H:%M:%S').")
class EmailField(BaseFieldDefinition):
    type: Literal["email"] = "email"
class NameField(BaseFieldDefinition):
    type: Literal["name"] = "name"
class AddressField(BaseFieldDefinition):
    type: Literal["address"] = "address"
class UUIDField(BaseFieldDefinition):
    type: Literal["uuid"] = "uuid"
class PhoneNumberField(BaseFieldDefinition):
    type: Literal["phone_number"] = "phone_number"
class EnumField(BaseFieldDefinition):
    type: Literal["enum"] = "enum"
    choices: List[str] = Field(..., min_length=1, description="List of possible values to choose from.")
# Forward declaration for recursive types
class ListField(BaseFieldDefinition):
    type: Literal["list"] = "list"
    item_definition: 'FieldDefinition' = Field(..., description="The definition of items within the list.")
    min_items: NonNegativeInt = Field(1, description="Minimum number of items in the list.")
    max_items: PositiveInt = Field(5, description="Maximum number of items in the list.")
class ObjectField(BaseFieldDefinition):
    type: Literal["object"] = "object"
    fields: List['FieldDefinition'] = Field(..., min_length=1, description="List of field definitions for the nested object.")
# --- Union Type for Polymorphism ---
# This allows Pydantic to validate based on the 'type' discriminator.
FieldDefinition = Annotated[
    Union[
        StringField,
        IntegerField,
        FloatField,
        BooleanField,
        DateField,
        DateTimeField,
        EmailField,
        NameField,
        AddressField,
        UUIDField,
        PhoneNumberField,
        EnumField,
        ListField,
        ObjectField,
    ],
    Field(discriminator='type')
]
# Update forward refs for recursive models
ListField.model_rebuild()
ObjectField.model_rebuild()
# --- Request and Response Models ---
class GenerateRequest(BaseModel):
    """
    Request model for generating synthetic data.
    """
    num_records: PositiveInt = Field(1, description="Number of synthetic records to generate.", le=1000)
    schema: List[FieldDefinition] = Field(..., min_length=1, description="A list of field definitions for the synthetic data structure.")
class GenerateResponse(BaseModel):
    """
    Response model for generated synthetic data.
    """
    data: List[Dict[str, Any]] = Field(..., description="The list of generated synthetic data records.")
#### `app/services/data_generator.py`
python
# app/services/data_generator.py
import random
from datetime import date, datetime, timedelta
from typing import Any, Dict, List
from faker import Faker
from app.models.data_schema import (
    GenerateRequest, FieldDefinition,
    StringField, IntegerField, FloatField, BooleanField,
    DateField, DateTimeField, EmailField, NameField, AddressField,
    UUIDField, PhoneNumberField, EnumField, ListField, ObjectField
)
from app.core.logging import get_logger
logger = get_logger(__name__)
class SyntheticDataGenerator:
    """
    Service responsible for generating synthetic data based on provided schema.
    """
    def __init__(self):
        self.fake = Faker()
    def _generate_value(self, field_def: FieldDefinition) -> Any:
        """
        Generates a single value based on the field definition.
        This method uses a match statement for cleaner type handling (Python 3.10+).
        For older Python versions, use if/elif.
        """
        try:
            match field_def:
                case StringField():
                    charset_map = {
                        "alphanumeric": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        "alpha": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                        "numeric": "0123456789",
                    }
                    chars = charset_map.get(field_def.charset.lower(), field_def.charset)
                    length = random.randint(field_def.min_length, field_def.max_length)
                    return ''.join(random.choice(chars) for _ in range(length))
                case IntegerField():
                    return random.randint(field_def.min_value, field_def.max_value)
                case FloatField():
                    return round(random.uniform(field_def.min_value, field_def.max_value), field_def.decimal_places)
                case BooleanField():
                    return random.choice([True, False])
                case DateField():
                    time_delta = field_def.end_date - field_def.start_date
                    random_days = random.randint(0, time_delta.days)
                    return (field_def.start_date + timedelta(days=random_days)).strftime(field_def.date_format)
                case DateTimeField():
                    time_delta = field_def.end_datetime - field_def.start_datetime
                    random_seconds = random.randint(0, int(time_delta.total_seconds()))
                    return (field_def.start_datetime + timedelta(seconds=random_seconds)).strftime(field_def.datetime_format)
                case EmailField():
                    return self.fake.email()
                case NameField():
                    return self.fake.name()
                case AddressField():
                    return self.fake.address()
                case UUIDField():
                    return str(self.fake.uuid4())
                case PhoneNumberField():
                    return self.fake.phone_number()
                case EnumField():
                    return random.choice(field_def.choices)
                case ListField():
                    num_items = random.randint(field_def.min_items, field_def.max_items)
                    return [self._generate_value(field_def.item_definition) for _ in range(num_items)]
                case ObjectField():
                    return {f.name: self._generate_value(f) for f in field_def.fields}
                case _:
                    logger.warning(f"Unknown field type encountered: {field_def.type}. Returning None.")
                    return None
        except Exception as e:
            logger.error(f"Error generating value for field '{field_def.name}' of type '{field_def.type}': {e}", exc_info=True)
            # Depending on requirements, you might want to raise, return None, or a default value
            raise ValueError(f"Failed to generate data for field '{field_def.name}' (type: {field_def.type}): {e}") from e
    def generate_records(self, request: GenerateRequest) -> List[Dict[str, Any]]:
        """
        Generates a list of synthetic data records based on the request schema.
        """
        generated_data = []
        for i in range(request.num_records):
            record = {}
            for field_def in request.schema:
                record[field_def.name] = self._generate_value(field_def)
            generated_data.append(record)
            logger.debug(f"Generated record {i+1}/{request.num_records}")
        logger.info(f"Successfully generated {request.num_records} records.")
        return generated_data
#### `app/api/v1/endpoints/synthetic_data.py`
python
# app/api/v1/endpoints/synthetic_data.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.data_schema import GenerateRequest, GenerateResponse
from app.services.data_generator import SyntheticDataGenerator
from app.core.logging import get_logger
logger = get_logger(__name__)
router = APIRouter()
# Dependency for the data generator service
def get_data_generator() -> SyntheticDataGenerator:
    """
    Provides an instance of the SyntheticDataGenerator.
    """
    return SyntheticDataGenerator()
@router.post(
    "/generate",
    response_model=GenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Synthetic Data",
    description="Generates a list of synthetic data records based on a provided schema and number of records.",
    response_description="A list of generated synthetic data records."
)
async def generate_synthetic_data(
    request: GenerateRequest,
    generator: SyntheticDataGenerator = Depends(get_data_generator)
) -> GenerateResponse:
    """
    Handles the request to generate synthetic data.
    - **request**: The `GenerateRequest` object containing `num_records` and `schema`.
    - **generator**: An instance of `SyntheticDataGenerator` injected via FastAPI's dependency injection.
    Returns a `GenerateResponse` containing the list of generated data.
    Raises `HTTPException` for internal server errors during data generation.
    """
    logger.info(f"Received request to generate {request.num_records} records with schema: {request.schema}")
    try:
        generated_data = generator.generate_records(request)
        return GenerateResponse(data=generated_data)
    except Exception as e:
        logger.exception(f"An error occurred during data generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate synthetic data: {e}"
        )
#### `app/api/v1/router.py`
python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import synthetic_data
api_v1_router = APIRouter()
api_v1_router.include_router(synthetic_data.router, tags=["Synthetic Data"])
#### `app/api/router.py`
python
# app/api/router.py
from fastapi import APIRouter
from app.api.v1.router import api_v1_router
api_router = APIRouter()
api_router.include_router(api_v1_router, prefix="/v1")
#### `.env.example`
APP_NAME="Synthetic Data Generator"
APP_VERSION="1.0.0"
DEBUG=True
---
### How to Use (Example Requests)
You can use `curl`, Postman, or the interactive Swagger UI (`/docs`) to test the API.
#### 1. Generate simple user data
**Endpoint:** `POST http://localhost:8000/api/v1/generate`
**Request Body:**
json
{
  "num_records": 3,
  "schema": [
    {
      "name": "user_id",
      "type": "uuid"
    },
    {
      "name": "full_name",
      "type": "name"
    },
    {
      "name": "email",
      "type": "email"
    },
    {
      "name": "age",
      "type": "integer",
      "min_value": 18,
      "max_value": 70
    },
    {
      "name": "is_active",
      "type": "boolean"
    },
    {
      "name": "registration_date",
      "type": "date",
      "start_date": "2020-01-01",
      "end_date": "2023-12-31",
      "date_format": "%Y/%m/%d"
    }
  ]
}
**Example `curl` command:**
bash
curl -X POST "http://localhost:8000/api/v1/generate" \
-H "Content-Type: application/json" \
-d '{
  "num_records": 3,
  "schema": [
    {
      "name": "user_id",
      "type": "uuid"
    },
    {
      "name": "full_name",
      "type": "name"
    },
    {
      "name": "email",
      "type": "email"
    },
    {
      "name": "age",
      "type": "integer",
      "min_value": 18,
      "max_value": 70
    },
    {
      "name": "is_active",
      "type": "boolean"
    },
    {
      "name": "registration_date",
      "type": "date",
      "start_date": "2020-01-01",
      "end_date": "2023-12-31",
      "date_format": "%Y/%m/%d"
    }
  ]
}'
**Example Response:**
json
{
  "data": [
    {
      "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "full_name": "Dr. Jane Doe",
      "email": "jane.doe@example.com",
      "age": 35,
      "is_active": true,
      "registration_date": "2021/05/15"
    },
    {
      "user_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef0",
      "full_name": "John Smith",
      "email": "john.smith@example.net",
      "age": 52,
      "is_active": false,
      "registration_date": "2020/11/01"
    },
    {
      "user_id": "c3d4e5f6-a7b8-9012-3456-7890abcdef01",
      "full_name": "Alice Johnson",
      "email": "alice.j@example.org",
      "age": 28,
      "is_active": true,
      "registration_date": "2023/02/28"
    }
  ]
}
#### 2. Generate data with nested objects and lists
**Endpoint:** `POST http://localhost:8000/api/v1/generate`
**Request Body:**
json
{
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
This comprehensive setup provides a robust, validated, and extensible backend for synthetic data generation, ready for production deployment.