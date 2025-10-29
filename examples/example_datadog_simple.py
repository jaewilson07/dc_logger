#!/usr/bin/env python3
"""
Example: Simple Datadog Logging with Environment Variables

This example demonstrates how to properly configure and use dc_logger to send
simple logs to Datadog using configuration from .env file.

This uses the DatadogHandler that actually sends logs to Datadog.

Prerequisites:
1. Create a .env file in the project root with:
   DATADOG_API_KEY=your_api_key_here
   DATADOG_APP_KEY=your_app_key_here (optional)
   DATADOG_SITE=datadoghq.com (or us3.datadoghq.com, datadoghq.eu, etc.)
   DATADOG_SERVICE=domolibrary (or your service name)
   DATADOG_ENV=production (or staging, development)

2. Install python-dotenv: pip install python-dotenv
"""

import asyncio
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")
    print("Install with: pip install python-dotenv")

from dc_logger.client.base import (
    Logger,
    HandlerInstance,
    set_global_logger,
)
from dc_logger.logs.services.cloud.datadog import DatadogServiceConfig, DatadogHandler


def setup_datadog_logger() -> Logger:
    """Setup Datadog logger with configuration from environment variables"""
    # Datadog configuration from .env
    datadog_config = DatadogServiceConfig(
        api_key=os.getenv("DATADOG_API_KEY"),
        app_key=os.getenv("DATADOG_APP_KEY"),  # Optional
        site=os.getenv("DATADOG_SITE", "datadoghq.com"),
        service=os.getenv("DATADOG_SERVICE", "domolibrary"),
        env=os.getenv("DATADOG_ENV", "production"),
    )

    # Create Datadog handler
    datadog_handler = DatadogHandler(config=datadog_config)

    # Create handler instance
    datadog_handler_instance = HandlerInstance(
        service_handler=datadog_handler,
        handler_name="datadog"
    )

    # Create logger with Datadog handler
    logger = Logger(
        app_name="datadog_example",
        handlers=[datadog_handler_instance]
    )

    # Set as global logger (optional, but useful for decorators)
    set_global_logger(logger)

    return logger


async def main():
    """Example of simple logging to Datadog"""
    print("=" * 70)
    print("Datadog Simple Logging Example")
    print("=" * 70)
    print()

    # Check if API key is configured
    api_key = os.getenv("DATADOG_API_KEY")
    if not api_key:
        print("ERROR: DATADOG_API_KEY not found in environment variables")
        print("Please set DATADOG_API_KEY in your .env file")
        return

    # Setup logger with Datadog handler
    print("Creating Datadog configuration from .env...")
    logger = setup_datadog_logger()

    # Get config for display (access via handler)
    datadog_config = logger.handlers[0].service_handler.cloud_config
    print(f"  Site: {os.getenv('DATADOG_SITE', 'datadoghq.com')}")
    print(f"  Service: {os.getenv('DATADOG_SERVICE', 'domolibrary')}")
    print(f"  Environment: {os.getenv('DATADOG_ENV', 'production')}")
    print(f"  API Key: {'Set' if api_key else 'Not Set'}")
    print()

    print("Logger initialized successfully!")
    print()

    # Send simple logs to Datadog
    print("Sending simple logs to Datadog...")
    print("-" * 70)

    # Example 1: Simple info log
    await logger.info(message="Application started successfully")
    print("[INFO] Log sent: Application started successfully")

    # Example 2: Simple warning log
    await logger.warning(message="High memory usage detected")
    print("[WARNING] Log sent: High memory usage detected")

    # Example 3: Simple error log
    await logger.error(message="Failed to connect to database")
    print("[ERROR] Log sent: Failed to connect to database")

    # Example 4: Simple info log with extra context
    await logger.info(
        message="User login successful",
        extra={"user_id": "user123", "login_method": "oauth2"}
    )
    print("[INFO] Log sent: User login successful (with extra context)")

    # Example 5: Simple debug log (requires show_debugging=True)
    logger.show_debugging = True  # Enable debug logs
    await logger.debug(message="Processing request: GET /api/data")
    print("[DEBUG] Log sent: Processing request: GET /api/data")

    print("-" * 70)
    print()

    # Flush remaining logs
    print("Flushing logs to Datadog...")
    await logger.handlers[0].flush()
    print("Logs flushed!")
    print()

    # Close logger
    print("Closing logger...")
    await logger.handlers[0].close()
    print("Logger closed.")
    print()

    print("=" * 70)
    print("Example completed!")
    print(f"Check your Datadog dashboard at {os.getenv('DATADOG_SITE', 'datadoghq.com')} to see the logs.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

