# Repo Purpose

`bazzarify-ansible` is a Python CLI orchestrator for two linked deployment concerns:
- build Docker images for Bazarify services
- deploy selected images to a remote host through Ansible

## What It Is
- A thin orchestration layer, not the source repo for the services it builds.
- A bridge between local build contexts, Docker image publishing, and remote stack refresh.
- A repo whose operational truth depends heavily on `.env` and `config/services.yaml`.

## What It Is Not
- It does not own application business logic for `vendor`, `consumer`, `frankenphp`, or other services.
- It does not define remote infrastructure topology beyond one logical Ansible host group and a deployment directory.
- It does not provision servers; it assumes the remote host already has Docker, Compose, SSH access, and a compose project directory.

## Primary User Flows
- Interactive mode from `main.py` for operators selecting presets or manual flows.
- Direct CLI mode for local scripts or CI-style execution.
- Direct module execution for build-only or deploy-only tasks.

## Core Outcome
- Turn service names plus target architecture into canonical image tags and optionally roll those images out remotely.
