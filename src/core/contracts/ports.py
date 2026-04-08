"""Narrow callable ports for orchestration dependencies."""

from typing import Callable
from src.core.domain.orchestration import BuildRequest, DeployRequest

BuildServicePort = Callable[[BuildRequest], None]
DeployImagesPort = Callable[[DeployRequest], None]
RunCommandPort = Callable[[list[str], str], None]
