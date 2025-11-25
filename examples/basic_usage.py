#!/usr/bin/env python3
"""
Basic Usage Example for dc_logger

This script demonstrates the fundamental usage patterns of dc_logger:
- Creating a logger with console output
- Logging at different levels
- Adding context to log messages
- Proper cleanup with logger.close()

Run this example:
    python basic_usage.py
"""

import asyncio

from dc_logger import ConsoleLogConfig, DCLogger, LogEntity, LogLevel


async def main() -> None:
    """Demonstrate basic dc_logger usage."""

    # =================================================================
    # Step 1: Create a logger with console configuration
    # =================================================================
    print("=" * 60)
    print("DC Logger - Basic Usage Example")
    print("=" * 60)
    print()

    # Create a console configuration
    # LogLevel.DEBUG shows all messages, use LogLevel.INFO for production
    config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        pretty_print=True,  # Makes JSON output readable
    )

    # Create the logger with your app name
    logger = DCLogger(config, app_name="basic_example")

    # =================================================================
    # Step 2: Log messages at different levels
    # =================================================================
    print(">>> Logging at different levels:")
    print()

    await logger.debug("This is a debug message - detailed info for developers")
    await logger.info("This is an info message - general operational info")
    await logger.warning("This is a warning - something might be wrong")
    await logger.error("This is an error - something failed")
    await logger.critical("This is critical - system-level failure")

    print()

    # =================================================================
    # Step 3: Add context to log messages
    # =================================================================
    print(">>> Logging with context:")
    print()

    # Log with user context
    await logger.info(
        "User logged in successfully",
        user="alice@example.com",
        action="user_login",
    )

    # Log with duration
    await logger.info(
        "Database query completed",
        action="db_query",
        duration_ms=150,
    )

    # Log with extra metadata
    await logger.info(
        "File processed",
        action="process_file",
        extra={
            "filename": "data.csv",
            "rows": 1000,
            "size_kb": 256,
        },
    )

    print()

    # =================================================================
    # Step 4: Log with entity information
    # =================================================================
    print(">>> Logging with entity context:")
    print()

    # Create an entity (represents something being operated on)
    dataset_entity = LogEntity(
        type="dataset",
        id="ds_12345",
        name="Sales Report Q4",
        additional_info={"owner": "analytics_team"},
    )

    await logger.info(
        "Dataset updated successfully",
        entity=dataset_entity,
        action="update_dataset",
        duration_ms=2500,
    )

    # Another entity example
    user_entity = LogEntity(
        type="user",
        id="usr_67890",
        name="Bob Smith",
    )

    await logger.info(
        "User profile updated",
        entity=user_entity,
        action="update_profile",
    )

    print()

    # =================================================================
    # Step 5: Always close the logger when done
    # =================================================================
    print(">>> Closing logger...")
    await logger.close()
    print("Logger closed successfully!")
    print()
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
