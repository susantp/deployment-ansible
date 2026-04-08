"""Concrete service wiring for orchestration ports."""

from dataclasses import dataclass
from src.core.contracts.ports import BuildServicePort, DeployImagesPort, RunCommandPort
from src.core.runtime.shell import run_command
from src.deploy.ansible import deploy_images
from src.docker.builder import build_service


@dataclass(frozen=True)
class ExecutionServices:
    """Concrete orchestration dependencies."""

    build_service: BuildServicePort
    deploy_images: DeployImagesPort
    run_command: RunCommandPort


DEFAULT_EXECUTION_SERVICES = ExecutionServices(
    build_service=lambda request: build_service(request, run_command=run_command),
    deploy_images=lambda request: deploy_images(request, run_command=run_command),
    run_command=run_command,
)
