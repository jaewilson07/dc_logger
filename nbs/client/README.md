# DC Logger Client - Decorator System

## Quick Start

```python
from dc_logger.client.decorators import log_call

# Simple usage
@log_call()
async def my_function():
    pass

# With configuration
@log_call(action_name="custom_action", include_params=True)
async def my_function(param1, param2):
    pass
```

## Files Structure

### `extractors.ipynb` / `extractors.py`
Contains all context extraction logic:
- **Abstract Interfaces**: Define contracts for extractors
  - `EntityExtractor` - Extract entity information
  - `HTTPDetailsExtractor` - Extract HTTP details
  - `MultiTenantExtractor` - Extract multi-tenant context
  - `ResultProcessor` - Process function results

- **Default Implementations**: Work with standard kwargs
  - `KwargsEntityExtractor`
  - `KwargsHTTPDetailsExtractor`
  - `KwargsMultiTenantExtractor`
  - `DefaultResultProcessor`

### `decorators.ipynb` / `decorators.py`
Contains decorator logic:
- `LogDecoratorConfig` - Configuration with dependency injection
- `log_call` - Main decorator function
- Helper functions for execution

## Why This Architecture?

### SOLID Principles

**Single Responsibility**: Each extractor handles ONE type of information  
**Open/Closed**: Extend via custom extractors without modifying core  
**Liskov Substitution**: Any extractor implementation works  
**Interface Segregation**: Separate interfaces for different concerns  
**Dependency Inversion**: Depends on abstractions, not implementations  

### Benefits

- **Platform Agnostic**: No hard-coded logic for any specific platform
- **Extensible**: Create custom extractors for your domain
- **Testable**: Each component can be tested independently
- **Maintainable**: Clear separation of concerns
- **Reusable**: Define extractors once, use everywhere

## Custom Extractors Example

```python
from dc_logger.client.extractors import EntityExtractor
from dc_logger.client.Log import LogEntity
from dc_logger.client.decorators import log_call, LogDecoratorConfig

class MyEntityExtractor(EntityExtractor):
    def extract(self, func, args, kwargs):
        # Your custom logic here
        obj = kwargs.get("my_object")
        if obj:
            return LogEntity(
                type="my_type",
                id=obj.id,
                name=obj.name
            )
        return None

# Use it
@log_call(config=LogDecoratorConfig(
    entity_extractor=MyEntityExtractor()
))
async def my_function(my_object):
    pass
```

## Documentation

See [DECORATOR_ARCHITECTURE.md](./DECORATOR_ARCHITECTURE.md) for complete documentation.

## Migration from Old Decorator

If you had a monolithic decorator with hard-coded logic:

**Before**:
```python
@log_function_call(...)
async def func(auth):
    # Decorator had hard-coded Domo logic
    pass
```

**After**:
```python
# Create domain-specific extractor
class MyExtractor(EntityExtractor):
    def extract(self, func, args, kwargs):
        # Your logic here
        pass

# Use with new decorator
@log_call(config=LogDecoratorConfig(
    entity_extractor=MyExtractor()
))
async def func(auth):
    pass
```

## Key Takeaways

1. **Extractors** handle "what to log" (separate responsibility)
2. **Decorator** handles "when to log" (execution flow)
3. **Configuration** ties them together (dependency injection)
4. **Platform-specific logic** goes in custom extractors (extensibility)
5. **Core logic stays clean** and platform-agnostic (maintainability)

