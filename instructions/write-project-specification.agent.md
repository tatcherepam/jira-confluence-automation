# Write Project Specification

Create a structured technical specification in Markdown from the user's requirements and relevant workspace context.

## Workflow

- Read the named requirements, design, and existing implementation files before drafting.
- Identify the product objective, audience, scope, constraints, assumptions, and acceptance criteria.
- Preserve confirmed decisions; mark unresolved decisions as open questions instead of inventing requirements.
- Keep implementation scope aligned with the existing project structure and technology choices.
- Use concrete, testable language and define behavior rather than vague aspirations.
- Include a clear distinction between in-scope and out-of-scope work.
- Include functional requirements, technical architecture, data contracts, state or data flow, error and empty states, accessibility, responsive behavior, performance, and verification.
- Define measurable formulas or rules for derived metrics where applicable.
- Include a recommended file structure when it will help implementation.
- Include acceptance criteria that can be checked by tests or manual verification.
- Determine the output path before drafting: if the user specifies a filename or path, use that exact path; otherwise save the result as `project_spec.md` in the project root.
- Never silently rename an explicitly requested output file or substitute the default filename after the user has provided a different path.
- Use ASCII by default and avoid unrelated file changes.

## Output Structure

Use these sections when applicable:

1. Document control
2. Objective
3. Scope and non-goals
4. User experience requirements
5. Technical architecture
6. Data contract
7. Metric and behavior definitions
8. Accessibility and responsive behavior
9. Performance and maintainability
10. Verification plan
11. Acceptance criteria

## Validation

- Check the Markdown for formatting or whitespace errors.
- Verify that every major requirement from the source material is represented.
- Verify that the file exists at the requested or default path and that its filename matches the instruction used.
- Report the exact output path and validation result after saving.
