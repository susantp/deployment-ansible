# Problem Statement

Verify that service selection now rejects malformed input and deduplicates repeated valid selections.

## Confirmed Facts

- Service parsing now validates token shape and range before returning services.
- Valid services are accumulated in input order only once.

## Assumptions

- Inspecting the downstream deploy command is sufficient to confirm deduplication because it shows the exact image list produced from selected services.

## Affected Files Or Modules

- `src/cli/menu.py`

## Solution Strategy

- Reproduce prior failure mode with mixed invalid input.
- Reproduce duplicate valid input and inspect the resulting downstream command.

## Verification Steps

- Ran:
  - `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`
- Ran invalid mixed-input flow:
  - manual mode
  - build
  - amd
  - services: `1 1 99 foo 2`
- Observed:
  - exited with `❌ Service selection out of range: '99'`
  - no build command started
- Ran duplicate valid-input flow:
  - manual mode
  - deploy
  - amd
  - services: `1 1 2`
- Observed downstream command:
  - `ansible-playbook ... --extra-vars {"docker_images": ["techbizz/nginx:latest-amd", "techbizz/redis:latest-amd"]}`
  - `nginx` appeared once even though `1` was entered twice
- Interrupted Ansible immediately after confirmation to avoid running a real deployment.

## Result

- Verification passed.
- Service selection now fails fast on malformed input and deduplicates repeated valid choices.
