"""Shared orchestration policies for image tags and supported architectures."""

ARCHITECTURE_PLATFORMS: dict[str, str] = {
    "amd": "linux/amd64/v2",
    "arm": "linux/arm64/v8",
}


def get_platform_for_arch(arch: str) -> str | None:
    """Resolve the Docker platform string for a supported architecture."""
    return ARCHITECTURE_PLATFORMS.get(arch)


def build_image_tag(service_name: str, arch: str) -> str:
    """Build the canonical image tag for a service and architecture."""
    return f"techbizz/{service_name}:latest-{arch}"
