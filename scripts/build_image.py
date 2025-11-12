#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from scripts.utils import run, load_env


def get_env_or_default(key: str, default: str) -> str:
    """Fetch from .env or environment with fallback."""
    return os.getenv(key, default)


def build_service(service_name: str, platform_arch: str):
    """Build and (optionally) push a single service image."""
    platforms = {"amd": "linux/amd64/v2", "arm": "linux/arm64/v8"}
    if platform_arch not in platforms:
        raise ValueError(f"Unsupported arch '{platform_arch}' — use amd or arm")

    platform = platforms[platform_arch]

    # Context paths (override via .env if needed)
    context_map = {
        "nginx": get_env_or_default("CONTEXT_NGINX", ""),
        "consumer": get_env_or_default("CONTEXT_CONSUMER", ""),
        "vendor": get_env_or_default("CONTEXT_VENDOR", ""),
        "frankenphp": get_env_or_default("CONTEXT_FRANKENPHP", ""),
        "postgres": get_env_or_default("CONTEXT_POSTGRES", ""),
        "postgres18": get_env_or_default("CONTEXT_POSTGRES18", ""),
    }

    if service_name not in context_map:
        raise ValueError(f"Unknown service '{service_name}'.")

    context_path = context_map[service_name]
    image_name = f"techbizz/{service_name}:latest-{platform_arch}"

    run(["docker", "buildx", "build", f"--platform={platform}", "-t", image_name, context_path],
        f"Building Docker image {image_name}")

    if platform_arch == "amd":
        run(["docker", "push", image_name], f"Pushing {image_name} to Docker Hub")
        run(["docker", "image", "rm", image_name], f"Cleaning up local {image_name}")


# ---------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python build_image.py <platform_arch> <service1> [service2] ...")
        print("Example: python build_image.py amd vendor consumer frankenphp")
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent
    load_env(project_root / ".env")

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
