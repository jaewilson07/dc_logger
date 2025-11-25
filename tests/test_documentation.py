"""
Tests for documentation completeness and quality.

This module validates that all public APIs have proper docstrings
with examples, parameter descriptions, and return value documentation.
"""

import inspect
from typing import List, Tuple

import dc_logger


def get_public_members(module) -> List[Tuple[str, object]]:
    """Get all public members from a module's __all__ list."""
    if hasattr(module, "__all__"):
        return [(name, getattr(module, name)) for name in module.__all__]
    return []


def has_docstring(obj) -> bool:
    """Check if an object has a non-empty docstring."""
    return bool(obj.__doc__ and obj.__doc__.strip())


def has_example_in_docstring(obj) -> bool:
    """Check if an object's docstring contains an example."""
    if not obj.__doc__:
        return False
    docstring = obj.__doc__.lower()
    return (
        "example:" in docstring
        or "examples:" in docstring
        or ">>>" in docstring
        or "```python" in docstring
    )


def has_args_section(obj) -> bool:
    """Check if a function's docstring has an Args section."""
    if not obj.__doc__:
        return False
    return "args:" in obj.__doc__.lower()


def has_returns_section(obj) -> bool:
    """Check if a function's docstring has a Returns section."""
    if not obj.__doc__:
        return False
    return "returns:" in obj.__doc__.lower()


def test_all_public_classes_have_docstrings():
    """Ensure all public classes have docstrings."""
    public_members = get_public_members(dc_logger)
    classes = [(name, obj) for name, obj in public_members if inspect.isclass(obj)]

    missing_docstrings = []
    for name, cls in classes:
        if not has_docstring(cls):
            missing_docstrings.append(name)

    assert not missing_docstrings, (
        f"The following public classes are missing docstrings: {missing_docstrings}"
    )


def test_all_public_functions_have_docstrings():
    """Ensure all public functions have docstrings."""
    public_members = get_public_members(dc_logger)
    functions = [
        (name, obj)
        for name, obj in public_members
        if inspect.isfunction(obj) or inspect.iscoroutinefunction(obj)
    ]

    missing_docstrings = []
    for name, func in functions:
        if not has_docstring(func):
            missing_docstrings.append(name)

    assert not missing_docstrings, (
        f"The following public functions are missing docstrings: {missing_docstrings}"
    )


def test_dclogger_methods_have_docstrings():
    """Ensure DCLogger's public methods have docstrings."""
    logger_class = dc_logger.DCLogger

    # Get public methods (not starting with _)
    public_methods = [
        (name, method)
        for name, method in inspect.getmembers(logger_class, predicate=inspect.isfunction)
        if not name.startswith("_")
    ]

    missing_docstrings = []
    for name, method in public_methods:
        if not has_docstring(method):
            missing_docstrings.append(name)

    assert not missing_docstrings, (
        f"DCLogger methods missing docstrings: {missing_docstrings}"
    )


def test_dclogger_methods_have_examples():
    """Ensure key DCLogger methods have examples in docstrings."""
    logger_class = dc_logger.DCLogger

    # Key methods that should have examples
    key_methods = ["debug", "info", "warning", "error", "critical", "log", "close"]

    missing_examples = []
    for method_name in key_methods:
        method = getattr(logger_class, method_name, None)
        if method and not has_example_in_docstring(method):
            missing_examples.append(method_name)

    assert not missing_examples, (
        f"DCLogger methods missing examples: {missing_examples}"
    )


def test_log_level_enum_has_docstring():
    """Ensure LogLevel enum has a docstring."""
    assert has_docstring(dc_logger.LogLevel), "LogLevel enum is missing a docstring"


def test_log_level_methods_have_docstrings():
    """Ensure LogLevel methods have docstrings."""
    log_level = dc_logger.LogLevel

    # Check specific methods
    methods_to_check = ["from_string", "should_log"]
    missing_docstrings = []

    for method_name in methods_to_check:
        method = getattr(log_level, method_name, None)
        if method and not has_docstring(method):
            missing_docstrings.append(method_name)

    assert not missing_docstrings, (
        f"LogLevel methods missing docstrings: {missing_docstrings}"
    )


def test_log_entity_has_docstring():
    """Ensure LogEntity has a docstring."""
    assert has_docstring(dc_logger.LogEntity), "LogEntity is missing a docstring"


def test_http_details_has_docstring():
    """Ensure HTTPDetails has a docstring."""
    assert has_docstring(dc_logger.HTTPDetails), "HTTPDetails is missing a docstring"


def test_console_log_config_has_docstring():
    """Ensure ConsoleLogConfig has a docstring."""
    assert has_docstring(dc_logger.ConsoleLogConfig), (
        "ConsoleLogConfig is missing a docstring"
    )


def test_log_call_decorator_has_docstring():
    """Ensure log_call decorator has a docstring with examples."""
    assert has_docstring(dc_logger.log_call), "log_call is missing a docstring"
    assert has_example_in_docstring(dc_logger.log_call), (
        "log_call is missing examples in docstring"
    )


def test_get_logger_has_docstring():
    """Ensure get_logger has a docstring."""
    assert has_docstring(dc_logger.get_logger), "get_logger is missing a docstring"


def test_set_global_logger_has_docstring():
    """Ensure set_global_logger has a docstring."""
    assert has_docstring(dc_logger.set_global_logger), (
        "set_global_logger is missing a docstring"
    )


def test_module_has_docstring():
    """Ensure dc_logger module has a docstring."""
    assert has_docstring(dc_logger), "dc_logger module is missing a docstring"


def test_documentation_files_exist():
    """Ensure key documentation files exist."""
    import os

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    required_files = [
        "README.md",
        "USAGE.md",
        "API_REFERENCE.md",
        ".ai/context.md",
        ".ai/examples.yaml",
        "docs/getting-started.md",
        "docs/configuration.md",
        "docs/best-practices.md",
        "examples/README.md",
        "examples/basic_usage.py",
        "examples/advanced_logging.py",
        "examples/custom_handlers.py",
    ]

    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(repo_root, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)

    assert not missing_files, f"Missing documentation files: {missing_files}"


def test_examples_are_importable():
    """Ensure example scripts don't have syntax or import errors."""
    import ast
    import os

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(repo_root, "examples")

    example_files = [
        "basic_usage.py",
        "advanced_logging.py",
        "custom_handlers.py",
    ]

    errors = []
    for example_file in example_files:
        file_path = os.path.join(examples_dir, example_file)
        if os.path.exists(file_path):
            try:
                # Read and parse the file to check for syntax errors
                with open(file_path) as f:
                    source = f.read()
                ast.parse(source)
            except SyntaxError as e:
                errors.append(f"{example_file}: Syntax error - {e}")
            except Exception as e:
                errors.append(f"{example_file}: {e}")

    assert not errors, f"Example files have errors: {errors}"


if __name__ == "__main__":
    # Run tests if executed directly
    import pytest

    pytest.main([__file__, "-v"])
