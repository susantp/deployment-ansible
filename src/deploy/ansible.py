"""Ansible deployment operations."""

import json
import subprocess
import sys
from src.core.config import PROJECT_ROOT
from src.core.domain.orchestration import DeployRequest
from src.core.contracts.ports import RunCommandPort
from src.core.runtime.shell import console, exit_with_message, fail, load_env


def deploy_images(
    request: DeployRequest,
    run_command: RunCommandPort,
) -> None:
    """Deploy Docker images using Ansible.

    Args:
        request: Deploy request containing image tags to deploy
    """
    # Project structure
    env_file = PROJECT_ROOT / ".env"
    config_dir = PROJECT_ROOT / "config"
    inventory_file = config_dir / "inventory.ini"
    playbook_file = config_dir / "pull-up-prune.yaml"

    if not inventory_file.exists():
        fail(f"Error: Inventory file not found: {inventory_file}")

    if not playbook_file.exists():
        fail(f"Error: Playbook file not found: {playbook_file}")

    # Load env vars
    load_env(env_file)

    extra_vars = {"docker_images": list(request.images)}

    # Prepare ansible-playbook command
    cmd = [
        "ansible-playbook",
        "-i",
        str(inventory_file),
        str(playbook_file),
        "--extra-vars",
        json.dumps(extra_vars),
    ]

    run_command(cmd, "Deploying Docker images with Ansible")


def main() -> None:
    """Main entry point for direct script execution."""
    # Require at least one docker image
    if len(sys.argv) < 2:
        fail("Usage: python -m src.deploy.ansible <image1[:tag]> [image2[:tag] ...]")

    docker_images = sys.argv[1:]
    from src.core.runtime.shell import run_command

    deploy_images(DeployRequest(images=tuple(docker_images)), run_command=run_command)


if __name__ == "__main__":
    main()
