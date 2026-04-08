#!/usr/bin/env python3
"""Main entry point for Bazarrify Deployment Tool."""

import subprocess
from rich.prompt import Prompt

from src.core.runtime.shell import print_header, console, load_env, exit_with_message
from src.cli.parser import parse_cli_args
from src.cli.menu import PRESETS, handle_manual_flow, handle_preset_flow
from src.cli.executor import execute_operation

from src.core.config import PROJECT_ROOT


def run_interactive_mode() -> tuple[str, str, list[str]]:
    """Run interactive menu mode.

    Returns:
        Tuple of (mode, arch, services)
    """
    print_header("Bazarrify Deployment Tool")

    # Display preset options
    for idx, preset in enumerate(PRESETS, 1):
        console.print(f"[green]{idx}.[/green] [bold white]{preset.name}[/bold white]")

    console.print("[green]0.[/green] [bold white]Manual / Custom[/bold white]")

    choice = Prompt.ask(f"\nSelect [green][0-{len(PRESETS)}][/green]")

    if choice == "0":
        return handle_manual_flow()
    else:
        return handle_preset_flow(PRESETS, choice)


def main() -> None:
    """Main application entry point."""
    load_env(PROJECT_ROOT / ".env")

    # Try CLI args first
    cli_result = parse_cli_args()

    if cli_result:
        mode = cli_result.mode
        arch = cli_result.arch
        services = cli_result.services
    else:
        mode, arch, services = run_interactive_mode()

    # Execute the operation
    execute_operation(mode, arch, services)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        exit_with_message(f"❌ Failed (exit {e.returncode})", e.returncode)
    except KeyboardInterrupt:
        exit_with_message("\n🛑 Interrupted by user.")
