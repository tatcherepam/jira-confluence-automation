## Motivation and Use Cases

- Keep instruction content platform-agnostic and store it in `./instructions/`.
- Use one instruction file for one focused SDLC workflow.
  + Split files that grow beyond roughly 700 lines or cover unrelated workflows.
  + Reference shared instructions with relative paths such as `./instructions/[name].agent.md`.
- Use `main.agent.md` as the catalog that routes tasks to relevant instructions.
  + Add Keywords for every catalog entry to improve instruction matching.
- Keep platform-specific files as thin adapters that reference the catalog or a leaf instruction.
- Reload the catalog on every prompt so changes take effect immediately.
- Extract stable, reusable workflows from productive agent sessions into new or updated instructions.

## Bootstrap Installation (New Project Setup)

- Detect the agent platform from project markers: `.github/` for VS Code + GitHub Copilot, `.cursor/` for Cursor, and `.claude/` for Claude Code.
- For VS Code + GitHub Copilot, create `.github/copilot-instructions.md`, `.github/prompts/`, `.vscode/settings.json`, and the catalog and meta-instruction under `instructions/`.
- Verify that the entry point references `./instructions/main.agent.md` and that the catalog lists `creating-instructions.agent.md`.
- Verify that settings enable instruction files and agent requests.
- Confirm: `Instruction infrastructure installed. You can now add more instructions following creating-instructions.agent.md.`

## General Concepts

- Instructions describe what to do; wrappers describe how to load them; the catalog describes when to use them.
- Use a tree of catalogs when the project has enough instructions to need subdomains.
- Keep the source of truth in `instructions/` when supporting multiple IDEs.

## Instructions

- Add new files to `./instructions/` using `[verb]-[subject].agent.md` naming.
- Use concise, actionable bullet points instead of long explanations.
- Write instruction content in English and respond to the user in their language.
- Add every new instruction to `./instructions/main.agent.md` with a one-line description and Keywords.
- Read an existing instruction before updating it; preserve useful content and make targeted edits.
- Test practical examples before documenting them.
- Keep each file focused and extract reusable workflows into separate instructions.

## Skills

- Use a skill instead of a plain instruction when the workflow needs executable code, reference documents, or reusable assets.
- Create skills under `./instructions/[name]/` with a required `SKILL.md` containing `name`, `description`, and `version` frontmatter.
- Add scripts, references, and assets only when they are needed.
- Register each skill in `./instructions/main.agent.md` and reference its `SKILL.md` from wrappers.

## VSCode + GitHub Copilot

- Add shortcuts under `./.github/prompts/` using `to-[name].prompt.md`.
- Use `agent: agent` frontmatter and reference the relevant instruction with a relative path.
- Keep `.github/copilot-instructions.md` focused on loading `./instructions/main.agent.md`.
- Include these workspace settings:
  + `github.copilot.chat.codeGeneration.useInstructionFiles`: `true`
  + `chat.mcp.access`: `all`
  + `chat.agent.maxRequests`: `250`

## Cursor

- Add always-applied rules under `./.cursor/rules/` with `alwaysApply: true` frontmatter.
- Make the main rule reference `./instructions/main.agent.md`.

## Claude Code

- Add commands under `./.claude/commands/` that reference the relevant instruction and accept `$ARGUMENTS`.
- Make `.claude/CLAUDE.md` reference `./instructions/main.agent.md`.
