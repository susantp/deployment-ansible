# Refactoring Summary

## Current State
The codebase has been refactored from a small pragmatic script-style layout into a clearer orchestrator with explicit boundaries.

## Main Improvements

### 1. Canonical Inputs
- operation and platform choices are centralized in `src/core/domain/choices.py`
- interactive mode and CLI mode resolve through the same domain choices

### 2. Shared Policy
- image naming and architecture mapping are centralized in `src/core/domain/policies.py`

### 3. Explicit Orchestration Planning
- build and deploy requests are modeled in `src/core/domain/orchestration.py`
- executor coordinates requests instead of building deploy tags inline

### 4. Dependency Contracts
- callable ports live in `src/core/contracts/ports.py`
- high-level orchestration no longer imports concrete infrastructure modules directly

### 5. Runtime Wiring
- concrete dependency wiring lives in `src/core/runtime/services.py`
- command execution and fail-fast runtime behavior live in `src/core/runtime/shell.py`

### 6. Adapter-Style Build and Deploy Modules
- `src/docker/builder.py` executes `BuildRequest`
- `src/deploy/ansible.py` executes `DeployRequest`

### 7. Directory Structure Alignment
`src/core/` now reflects architectural roles:

```text
src/core/
  config.py
  contracts/
  domain/
  runtime/
```

## What This Means For Developers
- if you need domain rules, look in `src/core/domain/`
- if you need runtime wiring or shell behavior, look in `src/core/runtime/`
- if you need execution contracts, look in `src/core/contracts/`
- if you need adapter behavior, look in `src/docker/` or `src/deploy/`

## Result
The repo is now easier to extend, easier to reason about, and much easier for a new developer to visualize from the filesystem alone.
