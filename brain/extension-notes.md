# Extension Notes

## Where To Change What
- Add or remove services in `config/services.yaml`, then add matching `.env` variables.
- Change CLI argument rules in `src/cli/parser.py`.
- Change interactive selection flow or presets in `src/cli/menu.py`.
- Change build semantics in `src/docker/builder.py`.
- Change deploy semantics in `src/deploy/ansible.py` or `config/pull-up-prune.yaml`.

## Couplings To Respect
- `src/cli/executor.py` assumes build and deploy share the same `techbizz/<service>:latest-<arch>` tag contract.
- `src/deploy/ansible.py` assumes `config/group_vars/remote.yaml` can resolve connection details from environment variables already loaded into the process.
- `config/services.yaml` and `.env.example` should evolve together; adding a service without its context variable creates a broken operator path.

## Likely Improvement Areas
- Push policy is asymmetric today: `amd` pushes, `arm` does not.
- CLI parsing does not validate mode or service names early; validation mostly happens deeper in execution.
- The manual `.env` parser is intentionally simple and may not handle advanced dotenv syntax.
- No automated test suite is present yet, despite docs describing a future testing layout.

## Product Vision
- The build pillar should stay oriented around image creation and registry publishing, even if registry selection is currently fixed to the existing naming contract.
- Future build work may add configurable image registry ownership, but that is vision-level direction, not an implemented contract yet.
- The deploy pillar is currently Docker-plus-Ansible focused, but the longer-term direction should leave room for additional deployment backends such as Kubernetes.
- Future deployment backends are a design direction only until a concrete plan, contract, and implementation are introduced.
- When extending toward new registries or new deployment targets, preserve the separation between orchestration planning and infrastructure adapters.
