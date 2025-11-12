#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path
from scripts.utils import load_env


def main():
    # Project structure assumptions
    project_root = Path(__file__).resolve().parent
    env_file = project_root.parent / ".env"
    config_dir = project_root.parent / "config"
    inventory_file = config_dir / "inventory.ini"
    playbook_file = config_dir / "pull-up-prune.yaml"
    # Load env vars
    load_env(env_file)

    # Require at least one docker image
    if len(sys.argv) < 2:
        print("⚠️  Usage: python deploy.py <image1[:tag]> [image2[:tag] ...]")
        sys.exit(1)

    docker_images = sys.argv[1:]
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


if __name__ == "__main__":
    main()
