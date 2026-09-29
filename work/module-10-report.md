# Module 10 Completion Report

## Instruction Files
    Directory: C:\workspace\hello-genai\instructions

    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    -a----          09/28/26     15:57            572 create-status-report.agent.md
    -a----          09/28/26     16:23           2197 create-technical-backlog.agent.md
    -a----          09/28/26     16:19           3675 creating-instructions.agent.md
    -a----          09/28/26     16:23           1300 main.agent.md
    -a----          09/28/26     16:23           1891 write-project-specification.agent.md

## main.agent.md Contents
# Instructions Catalog

Each entry below is an instruction file with a one-line description. Load the matching file when the request includes its keywords.

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — Create, organize, and maintain platform-agnostic instruction files and IDE adapters.
	+ Keywords: create instruction, update instruction, custom instructions, instruction catalog, Copilot setup
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Generate a concise weekly status report with fixed sections and format.
	+ Keywords: weekly status report, accomplishments, blockers, next week, team report
- [`./instructions/write-project-specification.agent.md`](./write-project-specification.agent.md) — Create a structured Markdown technical specification from project requirements.
	+ Keywords: project specification, technical specification, requirements document, acceptance criteria, data contract
- [`./instructions/create-technical-backlog.agent.md`](./create-technical-backlog.agent.md) — Break a project specification into a phased, actionable implementation backlog.
	+ Keywords: technical backlog, implementation backlog, phased plan, setup, core features, integration, testing, documentation

## Sample Instruction
- File: create-technical-backlog.agent.md
- Contents:
# Create Technical Backlog

Create a detailed, actionable implementation backlog in Markdown from a project specification.

## Workflow

- Read the complete project specification and inspect the relevant repository structure before drafting.
- Before creating the backlog, ask clarifying questions about priorities, phasing, integration scope, testing depth, and documentation scope when those decisions are not explicit.
- Preserve the user's confirmed priorities and record them near the top of the backlog.
- Organize work into these phases: Setup, Core Features, Integration, Testing, and Documentation.
- Make each task independently actionable and small enough to complete and verify in one focused change.
- Use Markdown checkboxes for every executable task: `- [ ]`.
- Add priorities such as P0, P1, or P2 when prioritization is known.
- Include dependencies, expected outcomes, and phase exit criteria where they improve execution.
- Translate requirements into implementation tasks for data, state, UI, behavior, error states, accessibility, responsive behavior, tests, and documentation.
- Keep Integration aligned with the specification; do not add live services, credentials, or APIs when they are out of scope.
- Include unit, component/integration, accessibility, responsive, end-to-end, and build checks when full testing is requested.
- Include both developer and user documentation when documentation scope includes both.
- Add a final definition of done tied to acceptance criteria.
- Save the result as `backlog.md` in the project root unless the user specifies another path.
- Use ASCII by default and avoid unrelated file changes.

## Required Sections

1. Delivery approach and confirmed priorities
2. Phase 1: Setup
3. Phase 2: Core Features
4. Phase 3: Integration
5. Phase 4: Testing
6. Phase 5: Documentation
7. Final definition of done

## Validation

- Verify every task is a checkbox.
- Check that all specification acceptance criteria map to at least one backlog task.
- Check for missing dependencies, vague wording, duplicate work, and scope violations.
- Validate Markdown formatting and report the output path after saving.
