import os
from pathlib import Path
import subprocess


def load_env(env_path: Path):
    """Load .env file manually into os.environ."""
    if not env_path.exists():
        print(f"⚠️  Warning: .env file not found at {env_path}")
        return
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def run(cmd: list[str], desc: str):
    """Run a shell command with clear feedback."""
    print(f"\n▶️  {desc}")
    subprocess.run(cmd, check=True)
    print(f"✅ {desc} completed.")
