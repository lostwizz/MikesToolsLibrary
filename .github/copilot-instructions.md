# MikesToolsLibrary Copilot Instructions

## Project Overview
MikesToolsLibrary is a Python logging library providing custom levels, colored console output, Unicode symbols, and extensible formatters. The core architecture centers on the `MikesLogging` module with modular components for setup, formatting, filtering, and decoration.

## Key Components
- **LoggerSetup**: Main class for configuring loggers with multiple output modes (console, file, rotating file, SMTP). Uses `LoggingMode` IntFlag for combining handlers.
- **CustomLevels**: Manages custom log levels (e.g., TRACE=25, DATA=26, SUCCESS=27) with associated colors and special characters.
- **CustomFormatter**: Handles color-coded console output, pretty-printing for complex objects (dicts, lists), and mode-specific formatting.
- **ExcludeLevelFilter**: Singleton filter for excluding log levels per `LoggingMode` (e.g., suppress DEBUG in production files).
- **LoggingMode**: IntFlag enum for handler types: `CONSOLE | ROTATINGFN` combines console and rotating file logging.

## Usage Patterns
- **Setup Logger**: `LoggerSetup(name="app", modes=LoggingMode.CONSOLE | LoggingMode.ROTATINGFN, maxBytes=100_000_000)`
- **Add Custom Level**: `CustomLevels.add("SUCCESS", 27, colorFmt="\033[32m", specialChar="✔")`
- **Filter Levels**: `ExcludeLevelFilter.turnOffLevel(logging.DEBUG, LoggingMode.FILE)` to exclude DEBUG from file logs
- **Import Path**: Always use absolute imports like `from MikesToolsLibrary.MikesLogging import LoggerSetup`
- **Decorator**: `@log_decorator` for automatic function entry/exit logging with custom levels

## Development Workflow
- **Build**: `pip install -e .` for editable install from src/ directory
- **Run Examples**: Execute `t.bat` to test loggerExample.py and versionExample.py
- **Version**: Dynamic from Git tags via Hatch VCS plugin; update by committing changes
- **Package Structure**: Source in `src/MikesToolsLibrary/`, examples in `examples/`, tests in `tests/` (currently empty)

## Conventions
- **Logging Levels**: Standard levels plus custom ones (25-29) with predefined colors/symbols
- **Handler Modes**: Combine with `|` operator; each mode gets its own filter instance
- **Formatter Modes**: `LoggingMode.CONSOLE` uses colors/symbols, `LoggingMode.FILE` uses plain text with timestamps
- **Singleton Filters**: `ExcludeLevelFilter` is shared across handlers; changes affect all matching modes
- **Pretty Printing**: Automatic for dicts/lists in log messages via `CustomFormatter._pp()`
- **Encoding**: All files use UTF-8; console output reconfigured for Unicode support

## Integration Points
- **External Deps**: None; pure Python logging extension
- **Cross-Module**: Logging components import from each other (e.g., CustomLevels updates CustomFormatter.COLORS)
- **Entry Points**: `basic-setup` script defined in pyproject.toml for example usage</content>
<parameter name="filePath">D:\_Python_Projects\MikesToolsLibrary\.github\copilot-instructions.md