"""Menu logic and interactive selection flows."""

from dataclasses import dataclass
from typing import Callable, Tuple, List
from rich.prompt import Prompt
from src.core.config import get_services_config
from src.core.domain.choices import OPERATION_CHOICES, PLATFORM_CHOICES, build_menu_options
from src.core.runtime.shell import print_header, console, fail
from src.cli.ui import select_from_menu

def get_services() -> list[str]:
    """Load services list from config."""
    config = get_services_config()
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
    seen_services = set()

    for idx_str in selected_indices:
        if not idx_str.isdigit():
            fail(f"Invalid service selection: '{idx_str}'")

        idx = int(idx_str) - 1
        if not 0 <= idx < len(services_list):
            fail(f"Service selection out of range: '{idx_str}'")

        service = services_list[idx]
        if service not in seen_services:
            services.append(service)
            seen_services.add(service)

    return services


def select_operation() -> str:
    """Prompt user to select operation mode."""
    options, display_options = build_menu_options(OPERATION_CHOICES)
    return select_from_menu(
        options,
        "Operation",
        "Invalid operation",
        display_options=display_options,
    )


def select_platform() -> str:
    """Prompt user to select platform architecture."""
    options, display_options = build_menu_options(PLATFORM_CHOICES)
    return select_from_menu(
        options,
        "Platform",
        "Invalid platform",
        display_options=display_options,
    )


def select_required_services() -> list[str]:
    """Select services and fail fast when none are chosen."""
    services = select_services()
    if not services:
        fail("No valid services selected.")
    return services


ServiceResolver = Callable[[], list[str]]


@dataclass(frozen=True)
class PresetSpec:
    """Declarative preset definition."""

    name: str
    operation: str
    platform: str
    resolve_services: ServiceResolver


PRESETS: tuple[PresetSpec, ...] = (
    PresetSpec(
        name="build-remote-{service}",
        operation="build",
        platform="amd",
        resolve_services=select_required_services,
    ),
    PresetSpec(
        name="deploy-remote-{service}",
        operation="deploy",
        platform="amd",
        resolve_services=select_required_services,
    ),
)


def handle_manual_flow() -> Tuple[str, str, List[str]]:
    """Handle manual/custom selection flow.

    Returns:
        Tuple of (mode, arch, services)
    """
    mode = select_operation()
    arch = select_platform()
    services = select_required_services()

    return mode, arch, services


def handle_preset_flow(
    presets: tuple[PresetSpec, ...], choice: str
) -> Tuple[str, str, List[str]]:
    """Handle preset selection flow.

    Args:
        presets: Available preset definitions
        choice: User's menu choice

    Returns:
        Tuple of (mode, arch, services)
    """
    try:
        preset_idx = int(choice) - 1
        if not (0 <= preset_idx < len(presets)):
            fail("Invalid preset selection.")

        preset = presets[preset_idx]
        mode = preset.operation
        arch = preset.platform
        services = preset.resolve_services()

        console.print(
            f"\n[bold magenta]🚀 Running Preset: {preset.name}[/bold magenta]"
        )
        console.print(f"   Operation: [cyan]{mode}[/cyan]")
        console.print(f"   Platform:  [cyan]{arch}[/cyan]")
        console.print(f"   Services:  [cyan]{', '.join(services)}[/cyan]")

        return mode, arch, services

    except ValueError:
        fail("Invalid input.")
