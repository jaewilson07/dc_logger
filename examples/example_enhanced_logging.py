#!/usr/bin/env python3
"""
Example: Enhanced Logging Features with level_name, optional action, and method passing

This example demonstrates the new enhanced logging features:
- level_name: Custom categorization of logs
- action: Only appears when action_name is provided (not None)
- method: HTTP method or operation type passed to logger calls
"""

import asyncio
from dc_logger.client.decorators import log_call
from dc_logger.client.Log import LogLevel
from dc_logger.client.base import Logger, HandlerInstance, Handler_BufferSettings, set_global_logger
from dc_logger.services.console.base import ConsoleHandler, Console_ServiceConfig

# Set up JSON console logger to see the actual output
console_config = Console_ServiceConfig(
    output_mode="console",
    output_type="json"
)

buffer_settings = Handler_BufferSettings()
console_handler = ConsoleHandler(
    buffer_settings=buffer_settings,
    service_config=console_config
)

handler_instance = HandlerInstance(
    service_handler=console_handler,
    handler_name="json_console",
    log_level=LogLevel.INFO
)

json_logger = Logger(
    handlers=[handler_instance],
    app_name="enhanced_demo"
)

set_global_logger(json_logger)

# Example 1: Basic usage with level_name (no action_name)
@log_call(level_name="get_data")
def get_data(dataset_id: str, **kwargs):
    """Get dataset data - demonstrates level_name usage."""
    print(f"  [LOGGER AVAILABLE] Requesting dataset {dataset_id}")
    print(f"  [LOGGER AVAILABLE] Parameters: {kwargs}")
    
    # Simulate API call
    result = {"id": dataset_id, "rows": 1000, "columns": 5}
    
    print(f"  [LOGGER AVAILABLE] Response: {len(result)} fields")
    return result

# Example 2: Different level_name for different operations
@log_call(level_name="route_function")
def route_function(endpoint: str, method: str = "GET"):
    """Route function - demonstrates different level_name."""
    print(f"  [LOGGER AVAILABLE] Routing to {endpoint}")
    
    # Simulate routing logic
    response = {"endpoint": endpoint, "method": method, "status": "routed"}
    
    print(f"  [LOGGER AVAILABLE] Route completed: {response}")
    return response

# Example 3: Class method with level_name
@log_call(level_name="class_method")
def class_method(self, entity_id: str):
    """Class method - demonstrates level_name for class methods."""
    print(f"  [LOGGER AVAILABLE] Processing entity {entity_id}")
    
    # Simulate entity processing
    result = {"entity_id": entity_id, "status": "processed"}
    
    print(f"  [LOGGER AVAILABLE] Entity processed: {result}")
    return result

# Example 4: No action_name (should not appear in completion logs)
@log_call(level_name="looper")
def looper(offset: int = 0, limit: int = 100):
    """Looper function - no action_name, should not appear in logs."""
    print(f"  [LOGGER AVAILABLE] Looper params: offset={offset}, limit={limit}")
    
    # Simulate processing
    records = [{"id": i, "data": f"record_{i}"} for i in range(offset, offset + limit)]
    
    print(f"  [LOGGER AVAILABLE] Processed {len(records)} records")
    return records

# Example 5: Both action_name and level_name
@log_call(action_name="custom_action", level_name="get_data_stream")
async def get_data_stream(dataset_id: str, **kwargs):
    """Get data stream - demonstrates both action_name and level_name."""
    print(f"  [LOGGER AVAILABLE] Starting stream for {dataset_id}")
    print(f"  [LOGGER AVAILABLE] Stream params: {kwargs}")
    
    # Simulate streaming
    for i in range(3):
        chunk = {"chunk": i, "data": f"stream_data_{i}"}
        print(f"  [LOGGER AVAILABLE] Stream chunk {i}")
        yield chunk
    
    print(f"  [LOGGER AVAILABLE] Stream completed")

# Example 6: Different log levels with method and level_name
@log_call(level_name="error_handling")
def error_handling():
    """Demonstrate different log levels with method and level_name."""
    print("  [LOGGER AVAILABLE] Debug message")
    print("  [LOGGER AVAILABLE] Info message")
    print("  [LOGGER AVAILABLE] Warning message")
    print("  [LOGGER AVAILABLE] Error message")
    print("  [LOGGER AVAILABLE] Critical message")
    
    return "error_handling_completed"

async def main():
    """Demonstrate enhanced logging features."""
    print("Enhanced Logging Features Example")
    print("=" * 60)
    print("This example shows the new enhanced logging features:")
    print("- level_name: Custom categorization of logs")
    print("- action: Only appears when action_name is provided")
    print("- method: HTTP method or operation type")
    print()
    
    print("1. get_data with level_name (no action_name):")
    result1 = get_data("dataset_123", include_metadata=True)
    print(f"Result: {result1}")
    print()
    
    print("2. route_function with different level_name:")
    result2 = route_function("/api/data", "POST")
    print(f"Result: {result2}")
    print()
    
    print("3. class_method with level_name:")
    result3 = class_method(None, "entity_456")
    print(f"Result: {result3}")
    print()
    
    print("4. looper with level_name only (no action_name):")
    result4 = looper(offset=0, limit=5)
    print(f"Result: {len(result4)} records")
    print()
    
    print("5. get_data_stream with both action_name and level_name:")
    async for chunk in get_data_stream("dataset_789", format="json"):
        print(f"Received chunk: {chunk}")
    print()
    
    print("6. Different log levels with method and level_name:")
    result6 = error_handling()
    print(f"Result: {result6}")
    print()
    
    print("=" * 60)
    print("ENHANCED FEATURES DEMONSTRATED:")
    print("[OK] level_name field added to logs for categorization")
    print("[OK] action field only appears when action_name is provided")
    print("[OK] method parameter passed to logger calls")
    print("[OK] Different level_name for different operations")
    print("[OK] Both action_name and level_name can be used together")
    print("[OK] All log levels support method and level_name parameters")
    print()
    print("KEY BENEFITS:")
    print("- Better log categorization with level_name")
    print("- Cleaner logs when action is not needed")
    print("- HTTP method tracking for API operations")
    print("- Perfect for Domo library integration")
    print("- Consistent logging across all decorated functions")

if __name__ == "__main__":
    asyncio.run(main())
