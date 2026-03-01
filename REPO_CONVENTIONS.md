# Repository Conventions

This repository stores reusable Codex skills and lightweight project instructions.

## What Belongs In Git

Commit only stable, reusable assets:

- `AGENTS.md`
- `README.md`
- `REPO_CONVENTIONS.md`
- skill source files such as `*/SKILL.md`, `*/agents/*.yaml`, and reusable references

Do not commit task-specific working artifacts, generated notes, or local machine state.

## Artifact Placement Rules

Use these locations consistently:

- skill logic: `.agents/skills/<skill-name>/`
- run control logs and stage reports: `<codex-cwd>/logs/runs/<run_id>/`
- project execution outputs: `<project-root>/runs/<run_id>/`
- project-specific notes and drafts: `docs/` or `workspace/` in project repos

If a file is specific to one task, one machine, one session, or one date, keep it out of skill directories.

## Skills Boundary

A skill directory should contain only reusable material:

- `SKILL.md`
- agent config
- reusable references/assets needed by the skill

Do not place these in a skill directory:

- project plans
- one-off experiment outputs
- temporary prompts
- session transcripts
- machine-specific setup notes

## Commit Hygiene

Before committing:

1. Check `git status`.
2. Remove or move task-specific artifacts from tracked paths.
3. Commit only reusable repository changes.

Preferred rule:

- commit the rule/skill
- do not commit run byproducts
