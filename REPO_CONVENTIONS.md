# Repository Conventions

This repository stores reusable Codex skills and lightweight project instructions.

## What Belongs In Git

Commit only stable, reusable assets:

- `AGENTS.md`
- `README.md`
- `REPO_CONVENTIONS.md`
- skill source files such as `*/SKILL.md`, `*/agents/*.yaml`, and long-lived references that are part of the skill itself

Do not commit task-specific working artifacts, generated notes, or local machine state.

## Artifact Placement Rules

Use these locations consistently:

- `docs/`: project-specific plans, briefs, meeting notes, scratch writeups, investigation logs
- `workspace/` or `WORKSPACE/`: local state, intermediate outputs, temp research material, caches, run notes
- skill directories under `.agents/skills/`, such as `.agents/skills/research-workflow/`: reusable skill logic only, not project outputs

If a file is specific to one task, one customer, one machine, one session, or one date, it should go under `docs/` or `workspace/`, not into a skill directory.

## Skills Boundary

A skill directory should contain only reusable material:

- `SKILL.md`
- agent config
- reusable reference material
- small helper assets that are necessary for the skill

Do not place these in a skill directory:

- project plans
- experiment outputs
- screenshots from one task
- temporary prompts
- session transcripts
- machine-specific setup notes

If the content teaches the skill how to operate across many tasks, keep it in the skill. If it only helps with the current task, put it in `docs/` or `workspace/`.

## Commit Hygiene

Before committing:

1. Check `git status`.
2. Remove or move task-specific artifacts out of tracked paths.
3. Commit only reusable repository changes.

Preferred rule:

- commit the rule or skill
- do not commit the byproducts of using the rule or skill

## Naming Guidance

For files under `docs/`:

- use descriptive names
- prefer date suffixes for snapshots, for example `project_plan_2026-02-28.md`

For files under `workspace/` or `WORKSPACE/`:

- optimize for convenience, not permanence
- assume they are disposable
