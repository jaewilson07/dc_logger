# Console Color Support

The dc_logger library now supports console colors for better visibility and readability of log output.

## Features

- **Default Colors**: Automatically applied based on log level
  - Green for DEBUG and INFO
  - Yellow for WARNING
  - Red for ERROR and CRITICAL
- **Custom Colors**: Override default colors with any supported color
- **Styled Colors**: Use bold, dim, italic, or underline styles
- **Works with all formats**: Both text and JSON output

## Supported Colors

Basic colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

Bright colors: `bright_black`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`

Aliases: `gray`, `grey` (same as `bright_black`)

## Supported Styles

Combine styles with colors using underscore: `bold_red`, `dim_blue`, `italic_green`, `underline_yellow`

Styles: `bold`, `dim`, `italic`, `underline`

## Usage Examples

### Using Logger Methods

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    config = ConsoleLogConfig(level=LogLevel.DEBUG, format="text")
    logger = DCLogger(config, "my_app")
    
    # Use default colors (green, yellow, red based on level)
    await logger.info("This is green")
    await logger.warning("This is yellow")
    await logger.error("This is red")
    
    # Override with custom colors
    await logger.info("Custom blue message", color="blue")
    await logger.warning("Custom magenta warning", color="magenta")
    
    # Use styled colors
    await logger.info("Bold red message", color="bold_red")
    await logger.error("Bold yellow error", color="bold_yellow")
    
    await logger.close()

asyncio.run(main())
```

### Using log_call Decorator

```python
from dc_logger import log_call

@log_call(color="bright_green")
def process_data(data_id: str):
    """This function's logs will be bright green"""
    return {"processed": data_id}

@log_call(color="bright_red")
def critical_operation():
    """This function's logs will be bright red"""
    return "completed"

@log_call()  # Uses default color based on log level
def normal_operation():
    """This function uses default green color"""
    return "done"
```

### Disabling Colors

To disable colors, simply don't specify the `color` parameter and the logger will use default colors. If you want no colors at all, you could:

1. Pipe output through a tool that strips ANSI codes
2. Set colors to empty string (though default colors will still apply)
3. Use JSON format which includes color in metadata but doesn't colorize the output itself

## Color in JSON Format

When using JSON format, the color is included as a field in the JSON output:

```python
config = ConsoleLogConfig(level=LogLevel.INFO, format="json", pretty_print=True)
logger = DCLogger(config, "my_app")

await logger.info("Message", color="blue")
# Output:
# {
#   "timestamp": "2025-11-06T20:00:00.000000Z",
#   "level": "INFO",
#   "message": "Message",
#   "color": "blue",
#   ...
# }
```

The entire JSON output will also be colorized in the console.

## Examples

See `examples/example_console_colors.py` for a complete working example.
