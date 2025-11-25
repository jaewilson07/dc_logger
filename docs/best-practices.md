# DC Logger Best Practices

Recommended patterns and practices for using dc_logger effectively.

## Table of Contents

- [General Guidelines](#general-guidelines)
- [Logging Patterns](#logging-patterns)
- [Structured Logging](#structured-logging)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Security](#security)
- [Testing](#testing)
- [Anti-Patterns](#anti-patterns)

## General Guidelines

### 1. Always Close the Logger

```python
# ✅ Good: Use try/finally
async def main():
    logger = DCLogger(config, "my_app")
    try:
        await run_application(logger)
    finally:
        await logger.close()

# ✅ Good: Context manager pattern
async def main():
    logger = DCLogger(config, "my_app")
    try:
        await logger.info("Starting")
        # Your code here
    finally:
        await logger.close()
```

### 2. Use Appropriate Log Levels

```python
# ✅ Good: Meaningful level selection
await logger.debug("Processing item", item_id=item.id)  # Debugging details
await logger.info("User logged in", user=user.email)    # Normal operation
await logger.warning("Retry attempt", attempt=3)        # Potential issue
await logger.error("Payment failed", order_id=order.id) # Error condition
await logger.critical("Database unavailable")           # System failure
```

### 3. Set Environment-Appropriate Levels

```python
# Development: Show everything
dev_config = ConsoleLogConfig(level=LogLevel.DEBUG)

# Production: INFO and above
prod_config = ConsoleLogConfig(level=LogLevel.INFO)

# Critical systems: WARNING and above
critical_config = ConsoleLogConfig(level=LogLevel.WARNING)
```

## Logging Patterns

### Use Structured Logging

```python
# ❌ Bad: String concatenation
await logger.info(f"User {user_id} purchased {item_name} for ${amount}")

# ✅ Good: Structured context
await logger.info(
    "Purchase completed",
    user=user_id,
    action="purchase",
    extra={
        "item": item_name,
        "amount": amount,
        "currency": "USD"
    }
)
```

### Use Entity Objects

```python
# ✅ Good: Entity provides consistent structure
entity = LogEntity(
    type="order",
    id=order.id,
    name=order.reference
)

await logger.info("Order processed", entity=entity, action="process_order")
await logger.info("Order shipped", entity=entity, action="ship_order")
```

### Use Decorators for Functions

```python
# ✅ Good: Automatic function logging
@log_call(action_name="process_payment", include_params=True)
async def process_payment(order_id: str, amount: float):
    # Automatically logs entry, exit, duration, and errors
    return await payment_service.charge(order_id, amount)
```

### Include Duration for Performance Tracking

```python
import time

start = time.time()
result = await expensive_operation()
duration_ms = int((time.time() - start) * 1000)

await logger.info(
    "Operation completed",
    action="expensive_operation",
    duration_ms=duration_ms
)
```

## Structured Logging

### Consistent Field Names

```python
# ✅ Good: Use consistent field names
await logger.info("API call", action="api_call", duration_ms=150)
await logger.info("DB query", action="db_query", duration_ms=50)

# ❌ Bad: Inconsistent field names
await logger.info("API call", operation="api_call", time_ms=150)
await logger.info("DB query", action="db_query", duration=50)
```

### Use HTTP Details for API Calls

```python
from dc_logger import HTTPDetails

# ✅ Good: Structured HTTP logging
http_details = HTTPDetails(
    method="POST",
    url="/api/v1/orders",
    status_code=201,
    response_size=1024
)

await logger.info("Order created", http_details=http_details)
```

### Use Extra for Custom Metadata

```python
# ✅ Good: Group related metadata
await logger.info(
    "File processed",
    action="process_file",
    extra={
        "file": {
            "name": "data.csv",
            "size_bytes": 10240,
            "rows": 1000
        },
        "processing": {
            "duration_ms": 500,
            "records_skipped": 5
        }
    }
)
```

## Error Handling

### Log Errors with Context

```python
# ✅ Good: Rich error context
try:
    result = await process_order(order_id)
except Exception as e:
    await logger.error(
        f"Order processing failed: {e}",
        entity=LogEntity(type="order", id=order_id),
        action="process_order",
        extra={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "stack_trace": traceback.format_exc()
        }
    )
    raise
```

### Use Appropriate Error Levels

```python
# Recoverable error
await logger.warning(
    "Retry scheduled",
    action="send_email",
    extra={"attempt": 2, "max_attempts": 3}
)

# Non-recoverable error
await logger.error(
    "Email delivery failed",
    action="send_email",
    extra={"error": str(e), "recipient": email}
)

# System-level failure
await logger.critical(
    "Email service unavailable",
    extra={"service": "sendgrid", "status": "down"}
)
```

### Error Logging Pattern

```python
async def safe_operation(data_id: str, logger: DCLogger):
    """Pattern for safe operations with logging."""
    entity = LogEntity(type="data", id=data_id)
    
    try:
        await logger.info("Starting operation", entity=entity, action="process")
        
        result = await perform_operation(data_id)
        
        await logger.info(
            "Operation completed",
            entity=entity,
            action="process",
            duration_ms=elapsed_ms,
            extra={"records": len(result)}
        )
        return result
        
    except ValidationError as e:
        await logger.warning(
            f"Validation failed: {e}",
            entity=entity,
            action="process"
        )
        raise
        
    except Exception as e:
        await logger.error(
            f"Operation failed: {e}",
            entity=entity,
            action="process",
            extra={"error_type": type(e).__name__}
        )
        raise
```

## Performance Considerations

### Use Batching for High-Volume Logging

```python
config = ConsoleLogConfig(
    batch_size=100,      # Buffer 100 logs before flush
    flush_interval=30    # Or flush every 30 seconds
)
```

### Avoid Expensive Operations in Log Messages

```python
# ❌ Bad: Expensive operation in log call
await logger.debug(f"Data: {expensive_serialization(data)}")

# ✅ Good: Check level first
if logger.config.level.should_log(LogLevel.DEBUG):
    await logger.debug(f"Data: {expensive_serialization(data)}")
```

### Use Async Properly

```python
# ✅ Good: Await log calls
await logger.info("Operation completed")

# ❌ Bad: Forgetting to await (logs may be lost)
logger.info("Operation completed")  # Missing await!
```

## Security

### Sanitize Sensitive Data

```python
# ✅ Good: Use sensitive_params in decorators
@log_call(
    sensitive_params=["password", "api_key", "token", "credit_card"]
)
async def authenticate(username: str, password: str):
    pass  # password logged as "***"
```

### Don't Log Secrets

```python
# ❌ Bad: Logging secrets
await logger.info(f"API key: {api_key}")

# ✅ Good: Log that you have a key, not the key itself
await logger.info("API key configured", extra={"key_prefix": api_key[:4] + "..."})
```

### Sanitize User Input

```python
# ✅ Good: Truncate potentially large user input
user_input = request.body[:500] if len(request.body) > 500 else request.body
await logger.info("Request received", extra={"body_preview": user_input})
```

## Testing

### Mock the Logger

```python
from unittest.mock import AsyncMock, MagicMock

async def test_my_function():
    mock_logger = MagicMock()
    mock_logger.info = AsyncMock()
    mock_logger.error = AsyncMock()
    
    await my_function(logger=mock_logger)
    
    mock_logger.info.assert_called()
```

### Test Log Output

```python
import io
import sys

async def test_log_output():
    # Capture stdout
    captured = io.StringIO()
    sys.stdout = captured
    
    try:
        logger = DCLogger(ConsoleLogConfig(), "test")
        await logger.info("Test message")
        await logger.flush()
        await logger.close()
        
        output = captured.getvalue()
        assert "Test message" in output
    finally:
        sys.stdout = sys.__stdout__
```

## Anti-Patterns

### ❌ Not Closing the Logger

```python
# ❌ Bad: Logger never closed, logs may be lost
async def main():
    logger = DCLogger(config, "app")
    await logger.info("Hello")
    # Missing: await logger.close()
```

### ❌ Over-Logging

```python
# ❌ Bad: Too much logging
for item in large_list:
    await logger.debug(f"Processing {item}")  # Thousands of logs!
    process(item)

# ✅ Good: Log summary
await logger.info(f"Processing {len(large_list)} items")
for item in large_list:
    process(item)
await logger.info("Processing completed")
```

### ❌ String Formatting for Structured Data

```python
# ❌ Bad: Loses structure
await logger.info(f"User {user.id} ({user.email}) logged in from {ip}")

# ✅ Good: Maintains structure
await logger.info(
    "User logged in",
    user=user.email,
    extra={"user_id": user.id, "ip": ip}
)
```

### ❌ Ignoring Return Values

```python
# ❌ Bad: Ignoring errors
try:
    result = operation()
except Exception:
    logger.error("Failed")  # Missing await!
    # Continues as if nothing happened
```

### ❌ Logging in Tight Loops

```python
# ❌ Bad: Performance impact
while True:
    data = await read_data()
    await logger.debug("Read data")  # Logs every iteration!
    process(data)

# ✅ Good: Log periodically
count = 0
while True:
    data = await read_data()
    count += 1
    if count % 1000 == 0:
        await logger.debug(f"Processed {count} items")
    process(data)
```

## Summary

1. **Always close** the logger
2. **Use structured logging** with entities and context
3. **Choose appropriate levels** for each message
4. **Sanitize sensitive data** using built-in features
5. **Use decorators** for automatic function logging
6. **Include duration** for performance tracking
7. **Log errors with context** for debugging
8. **Batch logs** for high-volume applications
9. **Test your logging** like other code
10. **Avoid anti-patterns** that hurt performance or lose data

## See Also

- [Configuration Guide](./configuration.md) - All configuration options
- [Getting Started](./getting-started.md) - Basic setup
- [AI Agent Guide](./ai-agent-guide.md) - Quick reference
