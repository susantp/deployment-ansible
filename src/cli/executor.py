"""Operation execution orchestrator."""

from dataclasses import dataclass
from typing import Callable
from src.core.domain.orchestration import plan_build_requests, plan_deploy_request
from src.core.runtime.shell import fail
from src.core.runtime.services import DEFAULT_EXECUTION_SERVICES, ExecutionServices


def execute_build(
    arch: str,
    services: list[str],
    execution_services: ExecutionServices = DEFAULT_EXECUTION_SERVICES,
) -> None:
    """Execute build operation for given services."""
    for request in plan_build_requests(arch, services):
        execution_services.build_service(request)


def execute_deploy(
    arch: str,
    services: list[str],
    execution_services: ExecutionServices = DEFAULT_EXECUTION_SERVICES,
) -> None:
    """Execute deploy operation for given services."""
    execution_services.deploy_images(plan_deploy_request(arch, services))


OperationHandler = Callable[[str, list[str]], None]


@dataclass(frozen=True)
class OperationSpec:
    """Declarative operation definition."""

    name: str
    handlers: tuple[OperationHandler, ...]


OPERATIONS: tuple[OperationSpec, ...] = (
    OperationSpec(
        name="build",
        handlers=(lambda arch, services: execute_build(arch, services),),
    ),
    OperationSpec(
        name="deploy",
        handlers=(lambda arch, services: execute_deploy(arch, services),),
    ),
    OperationSpec(
        name="both",
        handlers=(
            lambda arch, services: execute_build(arch, services),
            lambda arch, services: execute_deploy(arch, services),
        ),
    ),
)


OPERATION_BY_NAME: dict[str, OperationSpec] = {
    operation.name: operation for operation in OPERATIONS
}


def execute_operation(mode: str, arch: str, services: list[str]) -> None:
    """Execute the requested operation(s)."""
    operation = OPERATION_BY_NAME.get(mode)
    if operation is None:
        fail(f"Invalid operation: {mode}")

    for handler in operation.handlers:
        handler(arch, services)
