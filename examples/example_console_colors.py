#!/usr/bin/env python3
"""
Example: Console Color Support

This example demonstrates the console color functionality:
- Default colors based on log level (green for INFO/DEBUG, yellow for WARNING, red for ERROR/CRITICAL)
- Custom colors can override defaults
- Colors work with log_call decorator
- Styled colors (bold, dim, etc.)
"""

import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel, log_call


async def main():
    # Create console logger
    config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        format="text",
        pretty_print=False
    )
    logger = DCLogger(config, "demo_app")

    print("=== Default Log Colors ===")
    print("(Green for DEBUG/INFO, Yellow for WARNING, Red for ERROR/CRITICAL)")
    print()

    await logger.debug("Debug message - should be green")
    await logger.info("Info message - should be green")
    await logger.warning("Warning message - should be yellow")
    await logger.error("Error message - should be red")
    await logger.critical("Critical message - should be red")

    print()
    print("=== Custom Colors ===")
    print()

    await logger.info("Custom blue message", color="blue")
    await logger.info("Custom magenta message", color="magenta")
    await logger.info("Custom cyan message", color="cyan")

    print()
    print("=== Styled Colors ===")
    print()

    await logger.info("Bold red message", color="bold_red")
    await logger.info("Bold green message", color="bold_green")
    await logger.warning("Bold yellow warning", color="bold_yellow")

    print()
    print("=== Using log_call Decorator with Colors ===")
    print()

    @log_call(color="bright_cyan")
    def process_data(data_id: str):
        """Process data with custom color"""
        print(f"  Processing data: {data_id}")
        return {"status": "processed", "id": data_id}

    @log_call()  # Uses default green color
    def fetch_record(record_id: str):
        """Fetch record with default color"""
        print(f"  Fetching record: {record_id}")
        return {"record": record_id, "data": "example"}

    process_data("dataset_123")
    fetch_record("record_456")

    await logger.close()


if __name__ == "__main__":
    asyncio.run(main())
