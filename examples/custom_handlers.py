#!/usr/bin/env python3
"""
Custom Handlers Example for dc_logger

This script demonstrates how to work with dc_logger handlers:
- Using different handler configurations
- Multi-handler setup with custom settings
- Understanding handler types (console, file, cloud)
- Handler configuration options

Run this example:
    python custom_handlers.py
"""

import asyncio
import os
import tempfile

from dc_logger import (
    ConsoleLogConfig,
    DCLogger,
    LogLevel,
    MultiHandlerLogConfig,
    create_file_config,
)
from dc_logger.configs import HandlerConfig


async def demo_console_handler() -> None:
    """Demonstrate console handler configurations."""
    print("=" * 60)
    print("Console Handler Demo")
    print("=" * 60)
    print()

    # JSON format (default)
    print(">>> JSON Format (production-like):")
    json_config = ConsoleLogConfig(
        level=LogLevel.INFO,
        format="json",
        pretty_print=False,
    )
    json_logger = DCLogger(json_config, "json_demo")
    await json_logger.info("This is JSON formatted output")
    await json_logger.close()

    print()

    # Pretty JSON format (development)
    print(">>> Pretty JSON Format (development):")
    pretty_config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        format="json",
        pretty_print=True,
    )
    pretty_logger = DCLogger(pretty_config, "pretty_demo")
    await pretty_logger.info(
        "This is pretty-printed JSON",
        extra={"nested": {"key": "value", "number": 42}},
    )
    await pretty_logger.close()

    print()

    # Text format
    print(">>> Text Format:")
    text_config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        format="text",
    )
    text_logger = DCLogger(text_config, "text_demo")
    await text_logger.info("This is text formatted output")
    await text_logger.close()

    print()


async def demo_file_handler() -> None:
    """Demonstrate file handler configurations."""
    print("=" * 60)
    print("File Handler Demo")
    print("=" * 60)
    print()

    # Create temporary directory for logs
    log_dir = tempfile.mkdtemp()

    # File handler via factory function
    from dc_logger import create_file_config

    log_file = os.path.join(log_dir, "app.log")
    print(f">>> Writing to: {log_file}")

    file_config = create_file_config(
        file_path=log_file,
        level=LogLevel.INFO,
    )

    file_logger = DCLogger(file_config, "file_demo")

    await file_logger.info("First log entry")
    await file_logger.warning("Warning entry")
    await file_logger.error("Error entry")

    await file_logger.close()

    # Show file contents
    print()
    print("File contents:")
    print("-" * 40)
    with open(log_file) as f:
        print(f.read())

    print()


async def demo_multi_handler() -> None:
    """Demonstrate multi-handler configuration."""
    print("=" * 60)
    print("Multi-Handler Demo (Console + File)")
    print("=" * 60)
    print()

    # Create temporary file
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "multi_handler.log")

    # Method 1: Using factory function
    print(">>> Method 1: Using create_console_file_config()")
    from dc_logger import create_console_file_config

    config1 = create_console_file_config(
        file_path=log_file,
        level=LogLevel.DEBUG,
        pretty_print=True,
    )

    logger1 = DCLogger(config1, "factory_demo")
    await logger1.info("This goes to both console AND file")
    await logger1.close()

    print()

    # Method 2: Using MultiHandlerLogConfig directly
    print(">>> Method 2: Using MultiHandlerLogConfig")

    log_file2 = os.path.join(log_dir, "multi_handler2.log")

    # Note: HandlerConfig uses 'type' and 'config' with actual config objects
    # This is an advanced usage - prefer factory functions for simplicity
    console_cfg = ConsoleLogConfig(level=LogLevel.INFO, pretty_print=True)
    file_cfg = create_file_config(file_path=log_file2, level=LogLevel.INFO)

    config2 = MultiHandlerLogConfig(
        level=LogLevel.INFO,
        handlers=[
            HandlerConfig(type="console", config=console_cfg),
            HandlerConfig(type="file", config=file_cfg),
        ],
    )

    logger2 = DCLogger(config2, "multi_demo")
    await logger2.info("Multi-handler with explicit config")
    await logger2.warning("Both handlers receive this")
    await logger2.close()

    print()
    print(f"File contents of {log_file2}:")
    print("-" * 40)
    with open(log_file2) as f:
        print(f.read())

    print()


async def demo_handler_options() -> None:
    """Demonstrate various handler configuration options."""
    print("=" * 60)
    print("Handler Options Demo")
    print("=" * 60)
    print()

    # Batch size and flush interval
    print(">>> Batch Size and Flush Interval:")
    print("(Logs are buffered and flushed periodically or when buffer is full)")

    config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        batch_size=10,  # Flush after 10 logs
        flush_interval=5,  # Or every 5 seconds
        pretty_print=True,
    )

    logger = DCLogger(config, "batch_demo")

    for i in range(3):
        await logger.info(f"Batch message {i + 1}")

    # Force flush
    await logger.flush()
    print("(Manually flushed)")

    await logger.close()
    print()

    # Log level filtering
    print(">>> Log Level Filtering:")
    print("(Setting level to WARNING filters out DEBUG and INFO)")

    warn_config = ConsoleLogConfig(
        level=LogLevel.WARNING,
        pretty_print=True,
    )

    warn_logger = DCLogger(warn_config, "level_demo")

    await warn_logger.debug("This DEBUG message is filtered out")
    await warn_logger.info("This INFO message is filtered out")
    await warn_logger.warning("This WARNING message IS shown")
    await warn_logger.error("This ERROR message IS shown")

    await warn_logger.close()
    print()


async def demo_colored_console() -> None:
    """Demonstrate colored console output."""
    print("=" * 60)
    print("Colored Console Output Demo")
    print("=" * 60)
    print()

    config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        format="text",  # Colors work best with text format
    )

    logger = DCLogger(config, "color_demo")

    # Default colors based on log level
    print(">>> Default level-based colors:")
    await logger.debug("Debug - green")
    await logger.info("Info - green")
    await logger.warning("Warning - yellow")
    await logger.error("Error - red")
    await logger.critical("Critical - red")

    print()

    # Custom colors
    print(">>> Custom colors:")
    await logger.info("Blue message", color="blue")
    await logger.info("Magenta message", color="magenta")
    await logger.info("Cyan message", color="cyan")
    await logger.info("Bold green", color="bold_green")
    await logger.info("Bold yellow", color="bold_yellow")

    await logger.close()
    print()


async def main() -> None:
    """Run all handler demos."""
    print()
    print("DC Logger - Custom Handlers Example")
    print("====================================")
    print()
    print("This example demonstrates different handler configurations")
    print("and options available in dc_logger.")
    print()

    await demo_console_handler()
    await demo_file_handler()
    await demo_multi_handler()
    await demo_handler_options()
    await demo_colored_console()

    print("=" * 60)
    print("All handler demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
