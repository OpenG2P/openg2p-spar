# Extension Guide

## Overview

This guide explains how to extend and customize the SPAR Mapper Core library for specific use cases.

---

## Adding Custom Validation Rules

### Step 1: Create Custom Validator

```python
# services/custom_validations.py
from openg2p_fastapi_common.service import BaseService
from ..exceptions import LinkValidationException

class CustomValidations(BaseService):
    async def validate_custom_rule(self, data: dict) -> None:
        """Validate custom business rules."""
        if not self._check_custom_condition(data):
            raise LinkValidationException(
                validation_error_type="rjct_custom_rule",
                message="Custom validation rule failed"
            )
    
    def _check_custom_condition(self, data: dict) -> bool:
        # Implement your custom logic
        return True
```

### Step 2: Integrate into MapperService

```python
# In services/mapper.py
from .custom_validations import CustomValidations

class MapperService(BaseService):
    async def link(self, link_request: LinkRequest):
        custom_validator = CustomValidations.get_component()
        
        for single_link_request in link_request_payload.link_request:
            await custom_validator.validate_custom_rule({
                "id": single_link_request.id,
                "fa": single_link_request.fa
            })
```

---

## Creating Custom Exception Types

```python
# exceptions/exceptions.py
class CustomBusinessException(Exception):
    def __init__(self, code: str, message: str):
        self.validation_error_type = code
        self.message = message
        super().__init__(message)
```

---

## Extending Data Models

### Add Custom Fields

```python
# In openg2p-spar-models/models/id_fa_mapping.py
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column

class IdFaMapping(BaseORMModelWithTimes):
    # ... existing fields ...
    
    custom_field_1: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    custom_field_2: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )
```

### Update Schemas

```python
# In openg2p-spar-models/schemas/id_fa_mapping.py
from pydantic import BaseModel, ConfigDict

class IdFaMappingSchema(BaseModel):
    # ... existing fields ...
    custom_field_1: Optional[str] = None
    custom_field_2: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)
```

---

## Implementing Custom Strategy Patterns

```python
# helpers/custom_strategy_helper.py
import re
from typing import Dict

class CustomStrategyHelper:
    @staticmethod
    def construct_custom_id(components: Dict[str, str], pattern: str) -> str:
        """Construct ID using custom pattern."""
        result = pattern
        for key, value in components.items():
            result = result.replace(f"{{{key}}}", value)
        return result
    
    @staticmethod
    def deconstruct_custom_id(id_value: str, pattern: str) -> Dict[str, str]:
        """Deconstruct ID using custom pattern."""
        match = re.match(pattern, id_value)
        if not match:
            return {}
        return match.groupdict()
```

---

## Adding New API Endpoints

```python
# In bene-portal-api/controllers/custom_controller.py
from openg2p_fastapi_common.controller import BaseController
from openg2p_spar_mapper_core.services import MapperService

class CustomController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.tags += ["Custom"]
        self.router.prefix = "/custom"
        self.service = MapperService.get_component()
        
        self.router.add_api_route(
            "/custom-operation",
            self.custom_operation,
            methods=["POST"]
        )
    
    async def custom_operation(self, request: CustomRequest):
        """Custom operation endpoint."""
        return {"status": "success"}
```

### Register in App

```python
# In app.py
from .controllers import CustomController

class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CustomController().post_init()
```

---

## Database Customization

### Add Custom Indexes

```python
# In models/id_fa_mapping.py
from sqlalchemy import Index

class IdFaMapping(BaseORMModelWithTimes):
    # ... fields ...
    
    __table_args__ = (
        Index('idx_custom_field_1', 'custom_field_1'),
        Index('idx_id_fa_composite', 'id_value', 'fa_value'),
    )
```

### Create Custom Queries

```python
# In services/mapper.py
from sqlalchemy import select, and_

class MapperService(BaseService):
    async def custom_query(self, session: AsyncSession):
        """Execute custom database query."""
        stmt = select(IdFaMapping).where(
            and_(
                IdFaMapping.active == True,
                IdFaMapping.id_value.like("PREFIX%")
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()
```

---

## Caching Implementation

```python
# helpers/cache_helper.py
from functools import lru_cache
from typing import Optional

class CacheHelper:
    _cache: dict = {}
    
    @staticmethod
    def get(key: str) -> Optional[any]:
        """Get value from cache."""
        return CacheHelper._cache.get(key)
    
    @staticmethod
    def set(key: str, value: any, ttl: int = 3600) -> None:
        """Set value in cache with TTL."""
        CacheHelper._cache[key] = {
            "value": value,
            "ttl": ttl
        }
```

### Use in Services

```python
# In services/mapper.py
from ..helpers.cache_helper import CacheHelper

class MapperService(BaseService):
    async def resolve(self, resolve_request: ResolveRequest):
        cache_key = f"resolve_{resolve_request.id}"
        
        # Check cache
        cached = CacheHelper.get(cache_key)
        if cached:
            return cached
        
        # Fetch from database
        result = await self._resolve_from_db(resolve_request)
        
        # Store in cache
        CacheHelper.set(cache_key, result)
        
        return result
```

---

## Logging and Monitoring

```python
# In services/mapper.py
import logging

_logger = logging.getLogger("spar-mapper-custom")

class MapperService(BaseService):
    async def link(self, link_request: LinkRequest):
        _logger.info(f"Processing link request: {link_request.id}")
        
        try:
            result = await self._process_link(link_request)
            _logger.info(f"Link successful: {link_request.id}")
            return result
        except Exception as e:
            _logger.error(f"Link failed: {link_request.id}, Error: {str(e)}")
            raise
```

---

## Testing Custom Extensions

### Unit Test Template

```python
# tests/test_custom_service.py
import pytest
from openg2p_spar_mapper_core.services import CustomService

@pytest.mark.asyncio
async def test_custom_validation():
    service = CustomService()
    
    # Test valid data
    result = await service.validate_custom_rule({"valid": True})
    assert result is None
    
    # Test invalid data
    with pytest.raises(CustomBusinessException):
        await service.validate_custom_rule({"valid": False})
```

---

## Performance Optimization

### Query Optimization

```python
# Use eager loading
from sqlalchemy.orm import selectinload

stmt = select(IdFaMapping).options(
    selectinload(IdFaMapping.provider)
)
```

### Batch Processing

```python
def batch_process(items: List, batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield batch
```

---

## Best Practices

1. **Follow existing patterns** - Maintain consistency
2. **Add comprehensive tests** - Test all new functionality
3. **Document changes** - Update documentation
4. **Use type hints** - Maintain type safety
5. **Handle errors gracefully** - Use custom exceptions
6. **Log operations** - Add logging for debugging
7. **Optimize queries** - Use indexes and eager loading
8. **Version your changes** - Track API versions

---

## Common Pitfalls

- ❌ Modifying core services directly
- ❌ Not handling async/await properly
- ❌ Missing database migrations
- ❌ Ignoring error handling
- ❌ Not testing extensions
- ❌ Hardcoding configuration values

---

**Last Updated**: October 2024
**Version**: 1.0.0

