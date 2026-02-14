"""Operation execution orchestrator."""

from src.docker.builder import build_service
from src.deploy.ansible import deploy_images


def execute_build(arch: str, services: list[str]):
    """Execute build operation for given services."""
    for service in services:
        build_service(service, arch)


def execute_deploy(arch: str, services: list[str]):
    """Execute deploy operation for given services."""
    images = [f"techbizz/{service}:latest-{arch}" for service in services]
    deploy_images(images)


def execute_operation(mode: str, arch: str, services: list[str]):
    """Execute the requested operation(s)."""
    if mode in {"build", "both"}:
        execute_build(arch, services)

    if mode in {"deploy", "both"}:
        execute_deploy(arch, services)
