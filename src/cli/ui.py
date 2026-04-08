"""Reusable UI components for menu interactions."""

from typing import Dict, Optional
from rich.prompt import Prompt
from src.core.shell import console, print_header


def display_menu_options(options: Dict[str, str], header: str|None = None):
    """Display numbered menu options.

    Args:
        options: Dict mapping option numbers to descriptions
        header: Optional header to display above menu
    """
    if header:
        print_header(header)

    for num, desc in options.items():
        console.print(f"[green]{num}.[/green] {desc}")


def prompt_choice(options: Dict[str, str], prompt_text: str|None = None) -> str:
    """Prompt user to select from menu options.

    Args:
        options: Dict mapping option numbers to values
        prompt_text: Custom prompt text (auto-generated if None)

    Returns:
        The selected value from options dict
    """
    if prompt_text is None:
        numeric_options = [int(k) for k in options.keys() if k.isdigit()]
        min_option = min(numeric_options)
        max_option = max(numeric_options)
        prompt_text = f"Select [green][{min_option}-{max_option}][/green]"

    choice = Prompt.ask(f"\n{prompt_text}")
    if choice not in options:
        return ""
    return options[choice]


def select_from_menu(
    options: Dict[str, str],
    header: str | None,
    error_msg: str = "Invalid selection",
    display_options: Optional[Dict[str, str]] = None,
) -> str:
    """Display menu, prompt for choice, and validate.

    Args:
        options: Dict mapping option numbers to values
        header: Header to display above menu
        error_msg: Error message for invalid selection
        display_options: Optional mapping used only for menu rendering

    Returns:
        The selected value

    Raises:
        SystemExit: If invalid selection
    """
    menu_options = display_options or options
    display_menu_options(menu_options, header)
    selected = prompt_choice(options)

    if not selected:
        console.print(f"[bold red]❌ {error_msg}[/bold red]")
        import sys

        sys.exit(1)

    return selected
