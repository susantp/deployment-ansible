"""Pure orchestration request models and planning helpers."""

from dataclasses import dataclass
from src.core.domain.policies import build_image_tag


@dataclass(frozen=True)
class BuildRequest:
    """Request to build a single service for an architecture."""

    service_name: str
    arch: str


@dataclass(frozen=True)
class DeployRequest:
    """Request to deploy a set of precomputed image tags."""

    images: tuple[str, ...]


def plan_build_requests(arch: str, services: list[str]) -> tuple[BuildRequest, ...]:
    """Plan build requests for the selected services."""
    return tuple(BuildRequest(service_name=service, arch=arch) for service in services)


def plan_deploy_request(arch: str, services: list[str]) -> DeployRequest:
    """Plan the deploy request for the selected services."""
    return DeployRequest(
        images=tuple(build_image_tag(service_name=service, arch=arch) for service in services)
    )
