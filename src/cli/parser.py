"""Command-line argument parsing and validation."""

import sys
from typing import Tuple, List
from src.core.shell import console


def parse_cli_args() -> Tuple[str, str, List[str]] | None:
    """Parse command-line arguments.

    Returns:
        Tuple of (mode, arch, services) if CLI args provided, None otherwise
    """
    if len(sys.argv) <= 1:
        return None

    mode = sys.argv[1].lower()

    if len(sys.argv) < 4:
        console.print("[bold red]Usage: main.py <mode> <arch> <service>...[/bold red]")
        sys.exit(1)

    arch = sys.argv[2]
    services = sys.argv[3:]

    return mode, arch, services
