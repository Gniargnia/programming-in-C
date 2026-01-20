---
applyTo: '**'
---

# Project Context
This project manages an Ark: Survival Evolved dedicated server on Linux using:
- Strict, auditable Bash scripts (no hidden state, no implicit behavior)
- A Python menu orchestrator (subprocess-based, explicit error handling)
- Systemd services and timers for automation
- A reproducible, minimal, self-healing mod and server management pipeline

The code in this repository does NOT run in the repository directory.  
It is deployed and executed on a remote Linux VM under the user `arkserver`.

## Runtime Environment (must be respected)
- Ark server root: `/home/arkserver/arkserver`
- ShooterGame root: `/home/arkserver/arkserver/ShooterGame`
- Mods directory: `/home/arkserver/arkserver/ShooterGame/Content/Mods`
- Config directory: `/home/arkserver/arkserver/ShooterGame/Config`
- Saved directory: `/home/arkserver/arkserver/ShooterGame/Saved`
- Logs directory: `/home/arkserver/arkserver/logs`


- Custom scripts (runtime): `/home/arkserver/arkserver/core`
  - `ark-mods.sh`
  - `ark-backup.sh`
  - `ark-stop.sh`
  - `ark-update-check.sh`
  - `ark-core.sh`

- SteamCMD executable: `/home/arkserver/steamcmd/steamcmd.sh`
- Ark workshop content: `/home/arkserver/Steam/steamapps/workshop/content/346110`

The philosophy of the project:
- No magic, no assumptions, no silent failure
- Every action must be explicit, logged, and reversible
- Scripts must degrade safely and fail loudly with meaningful exit codes
- All generated code must be minimal, annotated, and auditable
- No reliance on repository-relative paths at runtime

# Coding Guidelines for the AI
When generating code, answering questions, or reviewing changes, the AI must follow these rules:

## 1. General Principles
- Prefer minimal, explicit, deterministic solutions.
- Never introduce hidden behavior, global state, or implicit defaults.
- Never assume the code runs in the repository directory.
- Always use the VM absolute paths defined in the Runtime Environment.
- Always explain the reasoning behind non-trivial decisions.
- Avoid unnecessary abstractions, frameworks, or dependencies.
- Maintain reproducibility: no hidden environment-specific assumptions.

## 2. Bash Guidelines
- Use strict mode (`set -euo pipefail`) unless explicitly justified.
- Validate all inputs, arguments, and paths before use.
- Always check exit codes and propagate failures.
- Use clear, auditable logging:
  - stdout for normal logs and machine-readable output
  - stderr for errors and diagnostics
- Avoid subshell complexity unless required.
- Prefer small, composable functions over monolithic scripts.
- Do not use repository-relative paths for runtime logic.

## 3. Python Guidelines
- Use `subprocess` with explicit command arrays, never `shell=True`.
- Capture stdout/stderr and return structured results (e.g. parsed JSON).
- Never swallow exceptions; raise or propagate with context.
- Keep functions as pure as possible; avoid hidden side effects.
- Use type hints and docstrings for clarity.
- Do not assume the current working directory is the repository root; use explicit absolute paths.

## 4. Systemd Guidelines
- Services must be minimal and explicit.
- Use `ExecStart=` with full absolute paths.
- Logs must go to journald; no silent failures.
- Timers must specify accuracy and jitter explicitly.
- Avoid environment files unless necessary and document them clearly.
- Assume units are deployed under `/etc/systemd/system`, not in the repo.

## 5. Mod and Server Management Pipeline Rules
- Detect missing, duplicated, or invalid mods deterministically.
- Install, validate, update, repair, and clean mods with explicit, ordered steps.
- Never assume a mod is installed or valid unless verified.
- Always produce machine-readable output (single-line JSON) for the Python orchestrator.
- Use strict, documented exit codes for all scripts.
- Fail fast if SteamCMD, workshop paths, or server paths are invalid.

## 6. When Reviewing Code
- Identify hidden assumptions, implicit paths, or silent failure paths.
- Suggest minimal diffs, not full rewrites.
- Highlight reproducibility, auditability, and deployment issues.
- Ensure all paths, permissions, and dependencies are explicit.
- Reject patterns that assume local repo execution instead of the VM environment.

## 7. When Answering Questions
- Provide step-by-step reasoning.
- Avoid vague reassurance; focus on evidence-based guidance.
- Offer rollback strategies when proposing changes.
- Maintain the project's philosophy of explicitness and auditability.
- When in doubt about environment or paths, refer to the Runtime Environment section.

## 8. Output Format Expectations
- Prefer diffs or patches when modifying existing files.
- Annotate code with concise comments explaining intent.
- Never introduce unrelated refactors unless explicitly requested.
- For scripts that communicate with the orchestrator:
  - Output a single-line JSON object on stdout
  - Use documented fields and exit codes
  - Do not mix human-readable text with machine-readable output.
