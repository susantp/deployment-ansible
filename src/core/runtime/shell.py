"""Shell command execution utilities."""

import os
import sys
import subprocess
from pathlib import Path
from typing import NoReturn
from rich.console import Console
from rich.panel import Panel

console = Console()


def fail(message: str, detail: str | None = None, exit_code: int = 1) -> NoReturn:
    """Print a formatted error message and terminate."""
    console.print(f"[bold red]❌ {message}[/bold red]")
    if detail:
        console.print(detail)
    raise SystemExit(exit_code)


def exit_with_message(message: str, exit_code: int = 1) -> NoReturn:
    """Terminate with a plain message."""
    if exit_code == 1:
        raise SystemExit(message)
    console.print(message)
    raise SystemExit(exit_code)


def load_env(env_path: Path) -> None:
    """Load .env file manually into os.environ."""
    if not env_path.exists():
        fail(
            f"Error: Environment file not found at {env_path}",
            "[yellow]Please create a .env file from .env.example[/yellow]",
        )
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def run_command(cmd: list[str], desc: str) -> None:
    """Run a shell command with clear feedback."""
    console.print(f"\n[bold cyan]▶️  {desc}[/bold cyan]")
    try:
        subprocess.run(cmd, check=True)
        console.print(f"[bold green]✅ {desc} completed.[/bold green]")
    except subprocess.CalledProcessError:
        fail(f"{desc} failed.")


def run(cmd: list[str], desc: str) -> None:
    """Backward-compatible command runner wrapper."""
    run_command(cmd, desc)


def print_header(title: str) -> None:
    """Print a styled header."""
    console.print(
        Panel(f"[bold white]{title}[/bold white]", border_style="blue", expand=False)
    )
