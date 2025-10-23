#!/usr/bin/env python3
"""
Example: Global Logger Injection in @log_call Decorated Functions

This example demonstrates how the injected logger always uses the current global logger,
and how changing the global logger affects all decorated functions.
"""

import asyncio
from dc_logger.client.decorators import log_call
from dc_logger.client.Log import LogLevel
from dc_logger.client.base import Logger, HandlerInstance, Handler_BufferSettings, set_global_logger, get_global_logger
from dc_logger.services.console.base import ConsoleHandler, Console_ServiceConfig
from dc_logger.logs.services.file import FileHandler, File_ServiceConfig

# Example functions that use the injected logger
@log_call
def process_order(order_id: str, customer_id: str):
    """Process an order - uses injected logger."""
    # For sync functions, we'll just demonstrate that logger is available
    print(f"  [LOGGER AVAILABLE] Processing order {order_id} for customer {customer_id}")
    
    # Simulate some business logic
    print("  [LOGGER AVAILABLE] Validating order details")
    print("  [LOGGER AVAILABLE] Checking inventory")
    print("  [LOGGER AVAILABLE] Processing payment")
    
    return f"order_{order_id}_processed"

@log_call
async def send_notification(user_id: str, message: str):
    """Send notification - uses injected logger."""
    await logger.info(f"Sending notification to user {user_id}: {message}")
    
    # Simulate async business logic
    await logger.info("Validating user permissions")
    await logger.info("Formatting message")
    await logger.info("Sending via email/SMS")
    
    return f"notification_sent_to_{user_id}"

@log_call
def calculate_tax(amount: float, tax_rate: float):
    """Calculate tax - uses injected logger."""
    print(f"  [LOGGER AVAILABLE] Calculating tax for amount ${amount} at rate {tax_rate}%")
    
    tax_amount = amount * (tax_rate / 100)
    print(f"  [LOGGER AVAILABLE] Tax calculated: ${tax_amount}")
    
    return tax_amount

async def main():
    """Demonstrate global logger injection behavior."""
    print("Global Logger Injection Example")
    print("=" * 60)
    print("This example shows how @log_call decorated functions")
    print("automatically use the current global logger.")
    print()
    
    # Step 1: Use default global logger
    print("Step 1: Using Default Global Logger")
    print("-" * 40)
    print("All functions will use the default console logger...")
    
    result1 = process_order("ORD-001", "CUST-123")
    result2 = await send_notification("USER-456", "Your order has been processed!")
    result3 = calculate_tax(100.0, 8.5)
    
    print(f"Order processing result: {result1}")
    print(f"Notification result: {result2}")
    print(f"Tax calculation result: ${result3}")
    print()
    
    # Step 2: Set a custom global logger with different app name
    print("Step 2: Setting Custom Global Logger")
    print("-" * 40)
    print("Creating a custom logger with app_name='production_app'...")
    
    # Create custom console logger
    console_config = Console_ServiceConfig(
        output_mode="console",
        output_type="json"  # Use JSON format for this example
    )
    
    buffer_settings = Handler_BufferSettings()
    console_handler = ConsoleHandler(
        buffer_settings=buffer_settings,
        service_config=console_config
    )
    
    handler_instance = HandlerInstance(
        service_handler=console_handler,
        handler_name="production_console",
        log_level=LogLevel.INFO
    )
    
    production_logger = Logger(
        handlers=[handler_instance],
        app_name="production_app"
    )
    
    # Set the custom logger as global
    set_global_logger(production_logger)
    print("[OK] Set custom global logger with app_name='production_app'")
    print("Now all functions will use this logger...")
    print()
    
    # Test the same functions - they should now use the custom logger
    result4 = process_order("ORD-002", "CUST-789")
    result5 = await send_notification("USER-101", "Welcome to our service!")
    result6 = calculate_tax(250.0, 10.0)
    
    print(f"Order processing result: {result4}")
    print(f"Notification result: {result5}")
    print(f"Tax calculation result: ${result6}")
    print()
    
    # Step 3: Set another global logger with file output
    print("Step 3: Setting File Logger as Global")
    print("-" * 40)
    print("Creating a file logger and setting it as global...")
    
    # Create file logger
    file_config = File_ServiceConfig(
        destination="example_logs/business_operations.json",
        output_mode="file",
        format="json",
        append=True
    )
    
    file_handler = FileHandler(
        buffer_settings=buffer_settings,
        service_config=file_config
    )
    
    file_handler_instance = HandlerInstance(
        service_handler=file_handler,
        handler_name="business_file",
        log_level=LogLevel.INFO
    )
    
    file_logger = Logger(
        handlers=[file_handler_instance],
        app_name="business_operations"
    )
    
    # Set the file logger as global
    set_global_logger(file_logger)
    print("[OK] Set file logger as global with app_name='business_operations'")
    print("Now all functions will log to the file...")
    print()
    
    # Test the functions again - they should now log to file
    result7 = process_order("ORD-003", "CUST-999")
    result8 = await send_notification("USER-888", "Thank you for your business!")
    result9 = calculate_tax(500.0, 7.5)
    
    print(f"Order processing result: {result7}")
    print(f"Notification result: {result8}")
    print(f"Tax calculation result: ${result9}")
    print()
    
    # Step 4: Demonstrate that the global logger can be changed at runtime
    print("Step 4: Runtime Logger Changes")
    print("-" * 40)
    print("Changing global logger back to console for debugging...")
    
    # Get the original default logger
    default_logger = get_global_logger()
    set_global_logger(default_logger)
    print("[OK] Switched back to default console logger")
    print()
    
    # Test one more time
    result10 = process_order("ORD-004", "CUST-DEBUG")
    print(f"Debug order result: {result10}")
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("[OK] All @log_call decorated functions automatically use the current global logger")
    print("[OK] You can change the global logger at any time with set_global_logger()")
    print("[OK] No need to redecorate functions or pass logger instances")
    print("[OK] Perfect for different environments (dev, staging, production)")
    print("[OK] Great for testing with different loggers")
    print()
    print("Key Benefits:")
    print("- Dynamic logger configuration")
    print("- Consistent logging across all decorated functions")
    print("- Easy environment switching")
    print("- No boilerplate logger passing")
    print()
    print("Check the 'example_logs/business_operations.json' file to see the file logs!")

if __name__ == "__main__":
    asyncio.run(main())
