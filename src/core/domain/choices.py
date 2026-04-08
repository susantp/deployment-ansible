"""Shared canonical choices for CLI and interactive flows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ChoiceSpec:
    """Canonical domain choice with a UI label."""

    value: str
    label: str


OPERATION_CHOICES: tuple[ChoiceSpec, ...] = (
    ChoiceSpec(value="build", label="Build"),
    ChoiceSpec(value="deploy", label="Deploy"),
    ChoiceSpec(value="both", label="Both"),
)

PLATFORM_CHOICES: tuple[ChoiceSpec, ...] = (
    ChoiceSpec(value="amd", label="AMD (linux/amd64)"),
    ChoiceSpec(value="arm", label="ARM (linux/arm64)"),
)


def get_choice_values(choices: tuple[ChoiceSpec, ...]) -> set[str]:
    """Return the canonical values for a choice collection."""
    return {choice.value for choice in choices}


def build_menu_options(choices: tuple[ChoiceSpec, ...]) -> tuple[dict[str, str], dict[str, str]]:
    """Build interactive menu mappings from canonical choices."""
    options: dict[str, str] = {}
    display_options: dict[str, str] = {}

    for index, choice in enumerate(choices, start=1):
        key = str(index)
        options[key] = choice.value
        display_options[key] = choice.label

    return options, display_options
