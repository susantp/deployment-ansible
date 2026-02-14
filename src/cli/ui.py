"""Reusable UI components for menu interactions."""

from typing import Dict
from rich.prompt import Prompt
from src.core.shell import console, print_header


def display_menu_options(options: Dict[str, str], header: str = None):
    """Display numbered menu options.

    Args:
        options: Dict mapping option numbers to descriptions
        header: Optional header to display above menu
    """
    if header:
        print_header(header)

    for num, desc in options.items():
        console.print(f"[green]{num}.[/green] {desc}")


def prompt_choice(options: Dict[str, str], prompt_text: str = None) -> str:
    """Prompt user to select from menu options.

    Args:
        options: Dict mapping option numbers to values
        prompt_text: Custom prompt text (auto-generated if None)

    Returns:
        The selected value from options dict
    """
    if not prompt_text:
        max_option = max(int(k) for k in options.keys() if k.isdigit())
        prompt_text = f"Select [green][0-{max_option}][/green]"

    choice = Prompt.ask(f"\n{prompt_text}")
    return options.get(choice)


def select_from_menu(
    options: Dict[str, str], header: str, error_msg: str = "Invalid selection"
) -> str:
    """Display menu, prompt for choice, and validate.

    Args:
        options: Dict mapping option numbers to values
        header: Header to display above menu
        error_msg: Error message for invalid selection

    Returns:
        The selected value

    Raises:
        SystemExit: If invalid selection
    """
    display_menu_options(options, header)
    selected = prompt_choice(options)

    if not selected:
        console.print(f"[bold red]❌ {error_msg}[/bold red]")
        import sys

        sys.exit(1)

    return selected
