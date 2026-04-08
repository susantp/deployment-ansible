"""Command-line argument parsing and validation."""

from dataclasses import dataclass
import sys
from typing import Callable
from src.core.domain.choices import OPERATION_CHOICES, PLATFORM_CHOICES, get_choice_values
from src.core.runtime.shell import fail


@dataclass(frozen=True)
class ParsedCommand:
    """Normalized CLI command payload."""

    mode: str
    arch: str
    services: list[str]


CommandParser = Callable[[list[str]], ParsedCommand]


@dataclass(frozen=True)
class CliCommand:
    """Declarative CLI command definition."""

    name: str
    parse: CommandParser


def parse_mode_arch_services(args: list[str]) -> ParsedCommand:
    """Parse the standard positional command shape."""
    if len(args) < 3:
        fail("Usage: main.py <mode> <arch> <service>...")

    mode = args[0].lower()
    arch = args[1]

    if mode not in get_choice_values(OPERATION_CHOICES):
        fail(f"Invalid operation: {mode}")

    if arch not in get_choice_values(PLATFORM_CHOICES):
        fail(f"Invalid platform: {arch}")

    return ParsedCommand(mode=mode, arch=arch, services=args[2:])


CLI_COMMANDS: tuple[CliCommand, ...] = (
    CliCommand(name="mode-arch-services", parse=parse_mode_arch_services),
)


def parse_cli_args() -> ParsedCommand | None:
    """Parse command-line arguments.

    Returns:
        Parsed command if CLI args provided, None otherwise
    """
    if len(sys.argv) <= 1:
        return None

    raw_args = sys.argv[1:]
    last_error: str | None = None

    for command in CLI_COMMANDS:
        try:
            return command.parse(raw_args)
        except SystemExit as exc:
            if exc.code is not None:
                last_error = str(exc.code)

    if last_error is not None:
        fail(last_error)

    fail("Unsupported CLI command.")
