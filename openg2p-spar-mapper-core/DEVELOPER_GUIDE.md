# Developer Guide

## Overview

The OpenG2P SPAR Mapper Core is a FastAPI-based microservice library implementing G2P Connect API standards for linking, resolving, updating, and unlinking beneficiary identities with their financial accounts.

### Key Capabilities

- **Link**: Create mappings between Beneficiary IDs and Financial Accounts
- **Resolve**: Query and retrieve FA information for given IDs
- **Update**: Modify existing ID-FA mappings
- **Unlink**: Remove mappings between IDs and FAs
- **DFSP Management**: Manage Digital Financial Service Providers
- **Strategy-based Construction**: Regex-based ID/FA construction/deconstruction
- **Async/Await**: Full async support for high-performance operations
- **G2P Connect Compliant**: Implements official G2P Connect API standards

---

## Architecture

### Project Structure

```
openg2p-spar-mapper-core/
├── src/openg2p_spar_mapper_core/
│   ├── services/
│   │   ├── mapper.py              # Link, Resolve, Update, Unlink
│   │   ├── request_validations.py # Request validation
│   │   ├── id_fa_mapping_validations.py
│   │   ├── response_helper.py     # Response formatting
│   │   └── dfsp_service.py        # DFSP provider management
│   ├── helpers/
│   │   └── strategy_helper.py     # ID/FA construction
│   ├── exceptions/
│   │   └── exceptions.py          # Custom exceptions
│   └── __init__.py
├── tests/
│   ├── test_async_mapper_controller.py
│   └── test_dfsp_service.py
├── pyproject.toml
└── README.md
```

### Core Components

#### 1. MapperService
Main service handling Link, Resolve, Update, Unlink operations.

```python
class MapperService(BaseService):
    async def link(link_request: LinkRequest) -> LinkResponse
    async def resolve(resolve_request: ResolveRequest) -> ResolveResponse
    async def update(update_request: UpdateRequest) -> UpdateResponse
    async def unlink(unlink_request: UnlinkRequest) -> UnlinkResponse
```

#### 2. RequestValidation
Unified validation for all request types.

```python
class RequestValidation(BaseService):
    def validate_request(request: Union[LinkRequest, UpdateRequest, ...])
```

#### 3. IdFaMappingValidations
Business logic validation for ID-FA mappings.

```python
class IdFaMappingValidations(BaseService):
    async def validate_link_request_payload(payload)
    async def validate_update_request_payload(payload)
```

#### 4. ResponseHelper
Constructs G2P-compliant responses with proper headers.

```python
class ResponseHelper(BaseService):
    def construct_response(data, status, reason_code)
    def construct_error_response(exception)
```

#### 5. DfspService
Manages Digital Financial Service Providers.

```python
class DfspService(BaseService):
    def get_all_providers()
    def get_provider_by_type(provider_type)
    def get_provider_values(provider_type, parent_id)
    def get_children(parent_id)
```

#### 6. StrategyHelper
Handles regex-based ID/FA construction/deconstruction.

```python
class StrategyHelper(BaseService):
    def construct_id(components, strategy)
    def deconstruct_id(id_value, strategy)
```

---

## Data Models

### IdFaMapping
Represents a link between a Beneficiary ID and Financial Account.

```python
class IdFaMapping(BaseORMModelWithTimes):
    id_value: str
    fa_value: str
    name: str
    phone_number: str
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    active: bool
```

### DfspProvider
Top-level provider types (BANK, EMAIL_WALLET, MOBILE_WALLET).

```python
class DfspProvider(BaseORMModelWithTimes):
    code: str
    name: str
    provider_type: ProviderType
    description: str
    validation_regex: str
```

### DfspProviderValue
Specific provider instances with hierarchical support.

```python
class DfspProviderValue(BaseORMModelWithTimes):
    code: str
    name: str
    provider_type: ProviderType
    parent_id: Optional[int]  # For hierarchical structure
    children: List[DfspProviderValue]
```

### Strategy
ID/FA construction strategies using regex patterns.

```python
class Strategy(BaseORMModelWithTimes):
    strategy_type: StrategyType  # ID or FA
    construct_strategy: str      # Regex pattern
    deconstruct_strategy: str    # Regex pattern
```

---

## API Request/Response Flow

### Link Request Flow

```
1. Client sends LinkRequest
   ↓
2. RequestValidation.validate_request()
   ↓
3. IdFaMappingValidations.validate_link_request_payload()
   ↓
4. MapperService.link() creates mapping
   ↓
5. ResponseHelper.construct_response()
   ↓
6. Return LinkResponse with G2P headers
```

### Response Format

```json
{
  "response_header": {
    "version": "1.0.0",
    "message": "Link successful",
    "action": "link",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "status": "success"
  },
  "response_body": {
    "response_payload": {
      "link_response": [...]
    }
  }
}
```

---

## Exception Handling

Custom exceptions for each operation:

```python
class LinkException(Exception)
class ResolveException(Exception)
class UpdateException(Exception)
class UnlinkException(Exception)
class LinkValidationException(Exception)
class ResolveValidationException(Exception)
```

---

## Database Integration

### Connection Setup

```python
from openg2p_fastapi_common.context import dbengine
from sqlalchemy.ext.asyncio import async_sessionmaker

engine = dbengine.get()
async_session = async_sessionmaker(engine, class_=AsyncSession)
```

### Query Example

```python
async with async_session() as session:
    stmt = select(IdFaMapping).where(
        IdFaMapping.id_value == "ID123"
    )
    result = await session.execute(stmt)
    mapping = result.scalar_one_or_none()
```

---

## Testing

### Unit Test Example

```python
@pytest.mark.asyncio
async def test_link_request():
    service = MapperService()
    request = LinkRequest(...)
    response = await service.link(request)
    assert response.response_header.status == "success"
```

### Running Tests

```bash
pytest tests/
pytest --cov=openg2p_spar_mapper_core tests/
```

---

## Configuration

### Environment Variables

```bash
SPAR_BENE_PORTAL_API_DB_DBNAME=openg2p_spar_db
SPAR_BENE_PORTAL_API_DB_USERNAME=postgres
SPAR_BENE_PORTAL_API_DB_PASSWORD=password
SPAR_BENE_PORTAL_API_DB_HOSTNAME=localhost
SPAR_BENE_PORTAL_API_DB_PORT=5432
```

### Settings Class

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_dbname: str
    db_username: str
    db_password: str
    db_hostname: str
    db_port: int
    
    class Config:
        env_file = ".env"
        env_prefix = "SPAR_BENE_PORTAL_API_"
```

---

## Best Practices

1. **Always use async/await** for database operations
2. **Validate input** at request level with Pydantic
3. **Use type hints** for all functions
4. **Handle exceptions** gracefully with custom exceptions
5. **Log operations** for debugging and monitoring
6. **Write tests** for all new functionality
7. **Follow G2P Connect standards** for API responses
8. **Use environment variables** for configuration
9. **Implement proper error codes** for failures
10. **Document code** with docstrings

---

## Common Tasks

### Adding a New Endpoint

1. Create controller method
2. Define request/response schemas
3. Add validation logic
4. Implement service method
5. Write tests
6. Update documentation

### Adding Custom Validation

1. Create validation method in service
2. Add to validation pipeline
3. Define custom exception
4. Write tests
5. Document validation rules

### Extending Data Models

1. Add fields to ORM model
2. Update Pydantic schemas
3. Create database migration
4. Update service methods
5. Write tests

---

## Troubleshooting

### Common Issues

**Database Connection Error**
- Check PostgreSQL is running
- Verify credentials in .env
- Check firewall rules

**Async/Await Issues**
- Ensure all database calls use async
- Use `async with` for sessions
- Don't mix sync and async code

**Validation Errors**
- Check request payload format
- Verify enum values
- Review Pydantic error messages

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [G2P Connect Standards](https://g2p-connect.org/)
- [OpenG2P Documentation](https://docs.openg2p.org/)

---

**Last Updated**: October 2024
**Version**: 1.0.0

