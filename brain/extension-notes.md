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
