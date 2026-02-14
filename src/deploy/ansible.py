"""Ansible deployment operations."""

import json
import subprocess
import sys
from src.core.config import PROJECT_ROOT
from src.core.shell import load_env


def deploy_images(docker_images: list[str]):
    """Deploy Docker images using Ansible.

    Args:
        docker_images: List of Docker images to deploy
    """
    # Project structure
    env_file = PROJECT_ROOT / ".env"
    config_dir = PROJECT_ROOT / "config"
    inventory_file = config_dir / "inventory.ini"
    playbook_file = config_dir / "pull-up-prune.yaml"

    from src.core.shell import console

    if not inventory_file.exists():
        console.print(f"[bold red]❌ Error: Inventory file not found: {inventory_file}[/bold red]")
        sys.exit(1)

    if not playbook_file.exists():
        console.print(f"[bold red]❌ Error: Playbook file not found: {playbook_file}[/bold red]")
        sys.exit(1)

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
