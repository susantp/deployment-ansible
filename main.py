#!/usr/bin/env python3
"""Main entry point for Bazarrify Deployment Tool."""
import subprocess
import sys
from rich.prompt import Prompt

from pathlib import Path
from src.core.shell import print_header, console, load_env
from src.cli.parser import parse_cli_args
from src.cli.menu import PRESETS, handle_manual_flow, handle_preset_flow
from src.cli.executor import execute_operation

PROJECT_ROOT = Path(__file__).resolve().parent


def run_interactive_mode() -> tuple[str, str, list[str]]:
    """Run interactive menu mode.
    
    Returns:
        Tuple of (mode, arch, services)
    """
    print_header("Bazarrify Deployment Tool")
    
    # Display preset options
    preset_keys = list(PRESETS.keys())
    for idx, key in enumerate(preset_keys, 1):
        console.print(f"[green]{idx}.[/green] [bold white]{key}[/bold white]")
    
    console.print("[green]0.[/green] [bold white]Manual / Custom[/bold white]")
    
    choice = Prompt.ask(f"\nSelect [green][0-{len(preset_keys)}][/green]")
    
    if choice == "0":
        return handle_manual_flow()
    else:
        return handle_preset_flow(preset_keys, choice)


def main():
    """Main application entry point."""
    load_env(PROJECT_ROOT / ".env")
    
    # Try CLI args first
    cli_result = parse_cli_args()
    
    if cli_result:
        mode, arch, services = cli_result
    else:
        mode, arch, services = run_interactive_mode()
    
    # Execute the operation
    execute_operation(mode, arch, services)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Failed (exit {e.returncode})")
    except KeyboardInterrupt:
        sys.exit("\n🛑 Interrupted by user.")
