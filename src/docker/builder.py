"""Docker image building operations."""

import os
import subprocess
import sys
from src.core.config import get_services_config, PROJECT_ROOT
from src.core.shell import run, load_env


def get_env_or_default(key: str, default: str) -> str:
    """Fetch from .env or environment with fallback."""
    return os.getenv(key, default)


def build_service(service_name: str, platform_arch: str):
    """Build and (optionally) push a single service image."""
    platforms = {"amd": "linux/amd64/v2", "arm": "linux/arm64/v8"}
    if platform_arch not in platforms:
        raise ValueError(f"Unsupported arch '{platform_arch}' — use amd or arm")

    platform = platforms[platform_arch]

    # Load services configuration
    config = get_services_config()

    services_data = config.get("services", {})
    if service_name not in services_data:
        raise ValueError(f"Unknown service '{service_name}'.")

    # Get context path from env using the key from config
    env_var = services_data[service_name]
    context_path = get_env_or_default(env_var, "")
    image_name = f"techbizz/{service_name}:latest-{platform_arch}"

    run(
        [
            "docker",
            "buildx",
            "build",
            f"--platform={platform}",
            "-t",
            image_name,
            context_path,
        ],
        f"Building Docker image {image_name}",
    )

    if platform_arch == "amd":
        run(["docker", "push", image_name], f"Pushing {image_name} to Docker Hub")
        run(["docker", "image", "rm", image_name], f"Cleaning up local {image_name}")


def main():
    """Main entry point for direct script execution."""
    if len(sys.argv) < 3:
        print(
            "Usage: python -m src.docker.builder <platform_arch> <service1> [service2] ..."
        )
        print("Example: python -m src.docker.builder amd vendor consumer frankenphp")
        sys.exit(1)

    load_env(PROJECT_ROOT / ".env")

    platform_arch = sys.argv[1]
    services = sys.argv[2:]

    for service in services:
        try:
            build_service(service, platform_arch)
        except Exception as e:
            print(f"❌ Failed to build {service}: {e}")
            sys.exit(1)

    print("\n🎉 All builds completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Command failed (exit {e.returncode})")
    except KeyboardInterrupt:
        sys.exit("\n🛑 Interrupted by user.")
