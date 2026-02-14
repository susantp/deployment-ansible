"""Menu logic and interactive selection flows."""

from pathlib import Path
from typing import Tuple, List
from rich.prompt import Prompt
from src.core.config import load_config
from src.core.shell import print_header, console
from src.cli.ui import select_from_menu, display_menu_options

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "services.yaml"

# Define Presets
PRESETS = {
    "build-remote-{service}": {
        "operation": "build",
        "platform": "amd",
        "service": "{service}",
    },
    "deploy-remote-{service}": {
        "operation": "deploy",
        "platform": "amd",
        "service": "{service}",
    },
}


def get_services() -> list[str]:
    """Load services list from config."""
    config = load_config(CONFIG_PATH)
    return list(config.get("services", {}).keys())


def select_services() -> list[str]:
    """Prompt user to select services."""
    services_list = get_services()
    print_header("Select Service(s)")
    for idx, service in enumerate(services_list, 1):
        console.print(f"[green]{idx}.[/green] {service}")

    svc_choice = Prompt.ask(
        f"\nSelect [green][1-{len(services_list)}][/green] (space-separated for multiple)"
    )
    selected_indices = svc_choice.split()
    services = []
    for idx_str in selected_indices:
        try:
            idx = int(idx_str) - 1
            if 0 <= idx < len(services_list):
                services.append(services_list[idx])
        except ValueError:
            pass

    return services


def select_operation() -> str:
    """Prompt user to select operation mode."""
    options = {"1": "build", "2": "deploy", "3": "both"}
    display_options = {"1": "Build", "2": "Deploy", "3": "Both"}
    display_menu_options(display_options, "Operation")
    return select_from_menu(options, None, "Invalid operation")


def select_platform() -> str:
    """Prompt user to select platform architecture."""
    options = {"1": "amd", "2": "arm"}
    display_options = {"1": "AMD (linux/amd64)", "2": "ARM (linux/arm64)"}
    display_menu_options(display_options, "Platform")
    return select_from_menu(options, None, "Invalid platform")


def handle_manual_flow() -> Tuple[str, str, List[str]]:
    """Handle manual/custom selection flow.

    Returns:
        Tuple of (mode, arch, services)
    """
    mode = select_operation()
    arch = select_platform()
    services = select_services()

    if not services:
        console.print("[bold red]❌ No valid services selected.[/bold red]")
        import sys

        sys.exit(1)

    return mode, arch, services


def handle_preset_flow(
    preset_keys: List[str], choice: str
) -> Tuple[str, str, List[str]]:
    """Handle preset selection flow.

    Args:
        preset_keys: List of available preset keys
        choice: User's menu choice

    Returns:
        Tuple of (mode, arch, services)
    """
    try:
        preset_idx = int(choice) - 1
        if not (0 <= preset_idx < len(preset_keys)):
            console.print("[bold red]❌ Invalid preset selection.[/bold red]")
            import sys

            sys.exit(1)

        preset_name = preset_keys[preset_idx]
        preset = PRESETS[preset_name]

        mode = preset["operation"]
        arch = preset["platform"]
        svc_template = preset["service"]

        # Handle dynamic service selection
        if "{service}" in svc_template:
            services = select_services()
            if not services:
                console.print("[bold red]❌ No valid services selected.[/bold red]")
                import sys

                sys.exit(1)
        else:
            services = [svc_template] if isinstance(svc_template, str) else svc_template

        console.print(
            f"\n[bold magenta]🚀 Running Preset: {preset_name}[/bold magenta]"
        )
        console.print(f"   Operation: [cyan]{mode}[/cyan]")
        console.print(f"   Platform:  [cyan]{arch}[/cyan]")
        console.print(f"   Services:  [cyan]{', '.join(services)}[/cyan]")

        return mode, arch, services

    except ValueError:
        console.print("[bold red]❌ Invalid input.[/bold red]")
        import sys

        sys.exit(1)
