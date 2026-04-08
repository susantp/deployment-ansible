"""Docker image building operations."""

import os
import subprocess
import sys
from pathlib import Path
from src.core.config import get_services_config, PROJECT_ROOT
from src.core.domain.orchestration import BuildRequest
from src.core.contracts.ports import RunCommandPort
from src.core.runtime.shell import load_env, console, exit_with_message, fail
from src.core.domain.policies import build_image_tag, get_platform_for_arch


def get_env_or_default(key: str, default: str) -> str:
    """Fetch from .env or environment with fallback."""
    return os.getenv(key, default)


def build_service(
    request: BuildRequest,
    run_command: RunCommandPort,
) -> None:
    """Build and (optionally) push a single service image."""
    service_name = request.service_name
    platform_arch = request.arch
    platform = get_platform_for_arch(platform_arch)
    if platform is None:
        fail(
            f"Error: Unsupported architecture '{platform_arch}'",
            "[yellow]Please use 'amd' or 'arm'[/yellow]",
        )

    # Load services configuration
    config = get_services_config()

    services_data = config.get("services", {})
    if service_name not in services_data:
        fail(f"Error: Unknown service '{service_name}'")

    # Get context path from env using the key from config
    env_var = services_data[service_name]
    context_path_str = get_env_or_default(env_var, "")

    if not context_path_str:
        fail(
            f"Error: Build context path not set for {service_name}",
            f"[yellow]Please check if {env_var} is defined in .env[/yellow]",
        )

    if not Path(context_path_str).exists():
        fail(f"Error: Build context path does not exist: {context_path_str}")

    image_name = build_image_tag(service_name, platform_arch)

    run_command(
        [
            "docker",
            "buildx",
            "build",
            f"--platform={platform}",
            "-t",
            image_name,
            context_path_str,
        ],
        f"Building Docker image {image_name}",
    )

    if platform_arch == "amd":
        run_command(
            ["docker", "push", image_name],
            f"Pushing {image_name} to Docker Hub",
        )
        run_command(
            ["docker", "image", "rm", image_name],
            f"Cleaning up local {image_name}",
        )


def main() -> None:
    """Main entry point for direct script execution."""
    if len(sys.argv) < 3:
        fail(
            "Usage: python -m src.docker.builder <platform_arch> <service1> [service2] ...",
            "Example: python -m src.docker.builder amd vendor consumer frankenphp",
        )

    load_env(PROJECT_ROOT / ".env")

    platform_arch = sys.argv[1]
    services = sys.argv[2:]

    for service in services:
        try:
            from src.core.runtime.shell import run_command

            build_service(
                BuildRequest(service_name=service, arch=platform_arch),
                run_command=run_command,
            )
        except Exception as e:
            fail(f"Failed to build {service}: {e}")

    console.print("\n🎉 All builds completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        exit_with_message(f"❌ Command failed (exit {e.returncode})", e.returncode)
    except KeyboardInterrupt:
        exit_with_message("\n🛑 Interrupted by user.")
