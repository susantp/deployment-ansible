"""Ansible deployment operations."""

import json
import subprocess
import sys
from pathlib import Path
from src.core.shell import load_env


def deploy_images(docker_images: list[str]):
    """Deploy Docker images using Ansible.

    Args:
        docker_images: List of Docker images to deploy
    """
    # Project structure
    project_root = Path(__file__).resolve().parent.parent.parent
    env_file = project_root / ".env"
    config_dir = project_root / "config"
    inventory_file = config_dir / "inventory.ini"
    playbook_file = config_dir / "pull-up-prune.yaml"

    # Load env vars
    load_env(env_file)

    extra_vars = {"docker_images": docker_images}

    # Prepare ansible-playbook command
    cmd = [
        "ansible-playbook",
        "-i",
        str(inventory_file),
        str(playbook_file),
        "--extra-vars",
        json.dumps(extra_vars),
    ]

    print("🚀 Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("✅ Deployment completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed (exit {e.returncode})")
        sys.exit(e.returncode)


def main():
    """Main entry point for direct script execution."""
    # Require at least one docker image
    if len(sys.argv) < 2:
        print(
            "⚠️  Usage: python -m src.deploy.ansible <image1[:tag]> [image2[:tag] ...]"
        )
        sys.exit(1)

    docker_images = sys.argv[1:]
    deploy_images(docker_images)


if __name__ == "__main__":
    main()
