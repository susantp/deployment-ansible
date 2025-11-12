#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from scripts.utils import run

PROJECT_ROOT = Path(__file__).resolve().parent
BUILD_MODULE = "scripts.build_image"  # PROJECT_ROOT / "scripts" / "build_image.py"
DEPLOY_MODULE = "scripts.ansible_deploy_remote"  # PROJECT_ROOT / "scripts" / "ansible_deploy_remote.py"


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else input(
        "Choose (build / deploy / both): "
    ).strip().lower()
    if mode not in {"build", "deploy", "both"}:
        sys.exit("❌ Invalid option.")

    if len(sys.argv) > 3:
        arch = sys.argv[2]
        services = sys.argv[3:]
    else:
        arch = input("Enter platform (amd / arm): ").strip()
        services = input("Enter services (space-separated): ").strip().split()

    if not services:
        sys.exit("❌ No services specified.")

    if mode in {"build", "both"}:
        run(["python3", "-m", BUILD_MODULE, arch] + services,
            f"Building {', '.join(services)} for {arch}")

    if mode in {"deploy", "both"}:
        for service in services:
            image = f"techbizz/{service}:latest-{arch}"
            run(["python3", "-m", DEPLOY_MODULE, image],
                f"Deploying {service} ({arch})")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Failed (exit {e.returncode})")
    except KeyboardInterrupt:
        sys.exit("\n🛑 Interrupted by user.")
