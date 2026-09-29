# Agent Instruction Toolkit Setup Guide

This guide explains how to create a reusable, self-updating instruction toolkit for an AI coding agent.

## What Each File Does

### `instructions/main.agent.md`

This is the instruction catalog and routing layer. It tells the agent which focused instruction file to load for a request.

Use it for:

- A one-line description of every instruction.
- Keywords that help match user requests to instructions.
- Links to instruction files using relative paths.

Keep it short. It should route work, not contain the full workflow.

### `instructions/creating-instructions.agent.md`

This is the meta-instruction for maintaining the toolkit. It explains naming, structure, registration, platform adapters, and how to create new instruction files consistently.

Use it when:

- Creating a new instruction.
- Updating an existing instruction.
- Adding a new workflow to the catalog.
- Reviewing whether an instruction belongs in a focused file or a skill.

### `instructions/[verb]-[subject].agent.md`

These are focused workflow instructions. Each file should describe one repeatable activity, such as creating a status report, writing a project specification, or creating a technical backlog.

## Setup Steps

### 1. Create the instruction directory

Create `instructions/` in the project root. Keep the source of truth there so different IDE adapters can reference the same workflow files.

### 2. Create the catalog

Create `instructions/main.agent.md` with:

- A short title or heading.
- One catalog entry per instruction.
- A relative link to each instruction file.
- A one-line description.
- A `Keywords` line for request matching.

The catalog should be reloaded whenever the agent starts a new request so new instructions are available immediately.

### 3. Create the meta-instruction

Create `instructions/creating-instructions.agent.md` to document the toolkit's own conventions. Include:

- File naming rules.
- How to keep workflows focused.
- How to update the catalog.
- When to use an instruction versus a skill.
- How platform-specific wrappers should reference the shared catalog.

This file prevents future instructions from drifting into inconsistent formats.

### 4. Create a focused workflow instruction

Name the file with a verb and subject, for example:

- `create-status-report.agent.md`
- `write-project-specification.agent.md`
- `create-technical-backlog.agent.md`

Include these parts:

- Purpose and trigger conditions.
- Required inputs and workspace files to inspect.
- Ordered workflow steps.
- Output format and destination.
- Validation rules.
- Boundaries and out-of-scope behavior.

Write concrete instructions. Replace vague guidance such as "make it good" with checks such as "include acceptance criteria and verify each requirement maps to a task."

### 5. Register the workflow

Add the new instruction to `main.agent.md` immediately after creating it. Include keywords users are likely to use, not only the exact filename.

Example:

```markdown
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Generate a concise weekly status report.
    + Keywords: weekly status report, accomplishments, blockers, next week
```

### 6. Add the platform entry point

For VS Code with GitHub Copilot, use `.github/copilot-instructions.md` as the thin entry point. It should tell the agent to load `./instructions/main.agent.md` completely and reload it for every prompt.

Do not duplicate the full workflow in the platform file. The catalog and leaf instructions are the source of truth.

### 7. Use the toolkit during work

When a request matches a keyword:

1. Load `main.agent.md`.
2. Identify the matching focused instruction.
3. Load that instruction completely.
4. Follow its workflow before editing files.
5. Validate the result using the instruction's checks.
6. Update the instruction if a stable improvement is discovered.

### 8. Keep the toolkit self-updating

After a useful workflow, capture stable lessons in the relevant instruction file. Update the catalog when files are added or renamed.

Good updates include:

- A missing validation step.
- A recurring repository convention.
- A clearer output structure.
- A decision rule that prevents repeated clarification.
- A command that was verified to work in this project.

Avoid recording temporary task details, secrets, or one-off implementation noise.

### 9. Validate the toolkit

Before considering the setup complete, check that:

- Every catalog link points to an existing file.
- Every instruction has one focused purpose.
- Instructions state their output format and validation steps.
- The platform entry point references the catalog.
- A sample request can be routed to the correct instruction.
- The instructions do not contradict the project or each other.

## Recommended Files

```text
.github/
  copilot-instructions.md
instructions/
  main.agent.md
  creating-instructions.agent.md
  agent-toolkit-setup-guide.md
  create-status-report.agent.md
  write-project-specification.agent.md
  create-technical-backlog.agent.md
```

  ## Reusable Meta-Instruction Example

  Use a rule like this in the meta-instruction or platform entry point:

  > Before acting, load `./instructions/main.agent.md` completely. Match the request to a focused instruction by keyword, load that instruction completely, follow its workflow, and validate the result. When creating or changing an instruction, update the catalog and verify that every referenced file exists.

  This rule is reusable because it defines how the instruction system operates regardless of the specific workflow being requested.

  ## Example Contents for Each Recommended File

  ### `.github/copilot-instructions.md`

  ```markdown
  - Always load `./instructions/main.agent.md` completely before acting.
  - Reload it for every prompt so catalog changes take effect.
  - Follow the matching focused instruction listed in the catalog.
  ```

  ### `instructions/main.agent.md`

  ```markdown
  # Instructions Catalog

  Load the matching instruction when the request includes its keywords.

  - [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Generate a weekly status report.
    + Keywords: weekly status report, accomplishments, blockers, next week
  - [`./instructions/write-project-specification.agent.md`](./write-project-specification.agent.md) — Write a technical specification.
    + Keywords: project specification, requirements document, acceptance criteria
  - [`./instructions/create-technical-backlog.agent.md`](./create-technical-backlog.agent.md) — Create an implementation backlog.
    + Keywords: technical backlog, implementation backlog, phased plan
  ```

  ### `instructions/creating-instructions.agent.md`

  ```markdown
  # Create and Maintain Instructions

  - Use one focused instruction file for one repeatable workflow.
  - Name files `[verb]-[subject].agent.md`.
  - Include inputs, ordered steps, output format, and validation.
  - Register every new instruction in `main.agent.md` with keywords.
  - Keep platform adapters thin and keep workflow truth in `instructions/`.
  ```

  ### `instructions/agent-toolkit-setup-guide.md`

  ```markdown
  # Agent Instruction Toolkit Setup Guide

  Explain the purpose of the catalog, meta-instruction, focused instructions,
  platform adapters, registration process, maintenance rules, and validation.
  Include examples so a new contributor can reproduce the setup without guesswork.
  ```

  ### `instructions/create-status-report.agent.md`

  ```markdown
  # Create Weekly Status Report

  - Output Markdown with Accomplishments, Blockers, and Next week sections.
  - Use bullet points only and keep the report under 20 lines.
  - Use a professional tone and remove filler language.
  - Include owners, dates, risks, and next actions when available.
  ```

  ### `instructions/write-project-specification.agent.md`

  ```markdown
  # Write Project Specification

  - Read the requirements and relevant repository files first.
  - Define objective, scope, architecture, data contract, verification, and acceptance criteria.
  - Preserve confirmed decisions and identify unresolved questions.
  - Save the result as `project_spec.md` and validate Markdown formatting.
  ```

  ### `instructions/create-technical-backlog.agent.md`

  ```markdown
  # Create Technical Backlog

  - Read the complete project specification before drafting.
  - Ask about priorities and phasing when they are unclear.
  - Organize tasks into Setup, Core Features, Integration, Testing, and Documentation.
  - Use actionable `- [ ]` tasks with priorities, dependencies, and phase exit criteria.
  - Save the result as `backlog.md` and verify specification coverage.
  ```

## Maintenance Model

Treat the toolkit as project documentation and lightweight process automation:

- The catalog changes when workflows change.
- Focused instructions change when repeatable practices improve.
- The setup guide changes when the toolkit architecture changes.
- Platform adapters stay thin and point to the shared source of truth.

This structure lets the agent remember both what to do and why the project uses that workflow.