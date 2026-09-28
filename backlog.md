# Jira Sprint Dashboard Implementation Backlog

## Delivery Approach

- Every phase must leave the application in a runnable, verifiable state.
- Work is ordered by the agreed priority: data foundation, executive visibility, interactive exploration, balanced MVP integration, then visual polish.
- Integration is limited to mock-data integration. Live Jira access, authentication, and API calls are not part of this backlog.
- Each task should be completed with the smallest focused change possible and verified before moving on.

## Phase 1: Setup

**Phase outcome:** A clean React/Vite development environment runs locally and is ready for feature work.

- [ ] **P0** Confirm the `jira-dashboard/` directory is the isolated application root and document the existing entry points.
- [ ] **P0** Verify Node.js and npm versions used by the project and record the commands needed to run the app.
- [ ] **P0** Install the declared npm dependencies from `package-lock.json`.
- [ ] **P0** Confirm `npm.cmd run dev` starts the application at the configured local URL.
- [ ] **P0** Confirm `npm.cmd run build` creates a production build without errors.
- [ ] **P1** Remove unused Vite starter assets and imports that are not needed by the dashboard.
- [ ] **P1** Establish the source structure for data, derived metrics, shared UI components, and styles.
- [ ] **P1** Add or confirm formatting and linting commands in `package.json`.

**Phase 1 exit criteria:** A new contributor can install dependencies, start the app, and produce a successful production build using documented commands.

## Phase 2: Core Features

**Phase outcome:** The dashboard renders a complete current-sprint executive view from local mock data.

### 2.1 Data Foundation - highest priority

- [ ] **P0** Create a dedicated mock dataset module under `jira-dashboard/src/data/`.
- [ ] **P0** Add one active two-week sprint with ID, name, program, start date, end date, expected completion date, scope-change hours, and active status.
- [ ] **P0** Add Team Alpha, Team Beta, and Team Gamma records or team identifiers.
- [ ] **P0** Add work items covering all required statuses: `To Do`, `In Progress`, and `Done`.
- [ ] **P0** Add work items across multiple epics and owners.
- [ ] **P0** Add estimated hours and remaining hours for every work item.
- [ ] **P0** Add green, amber, and red risk values, including at least one blocker or dependency.
- [ ] **P0** Define a stable data contract for sprint, work item, team, epic, owner, and risk fields.
- [ ] **P0** Implement pure selectors or utility functions for total hours, remaining hours, completed hours, completion percentage, status totals, team totals, and risk precedence.
- [ ] **P0** Handle an empty filtered result without `NaN`, broken layout, or misleading totals.

### 2.2 Executive Visibility

- [ ] **P0** Build the page shell with program identity, data freshness context, current sprint name, date range, and days remaining.
- [ ] **P0** Build the headline KPI row for overall completion, expected finish, scope change, and delivery risk.
- [ ] **P0** Connect the completion KPI to calculated completed and total hours.
- [ ] **P0** Display the expected completion date from sprint data.
- [ ] **P0** Display scope-change hours and percentage with clear added/removed semantics.
- [ ] **P0** Display aggregate RAG status using red-over-amber-over-green precedence.
- [ ] **P0** Build the team comparison surface for all three teams.
- [ ] **P0** Show team completion percentage, total estimated hours, remaining hours, item count, and text-labelled RAG state.
- [ ] **P1** Build the effort-by-status visualization for To Do, In Progress, and Done.
- [ ] **P1** Add a concise delivery signal that explains the current progress shape in plain language.

### 2.3 Interactive Exploration

- [ ] **P1** Add a team filter with an All teams option and all three team values.
- [ ] **P1** Add a sprint filter with the active sprint represented and a structure that can accept future sprint values.
- [ ] **P1** Add an epic filter whose options are derived from the dataset.
- [ ] **P1** Add an owner filter whose options are derived from the dataset.
- [ ] **P1** Keep selected filter state in React state and derive all visible metrics from the filtered items.
- [ ] **P1** Add expandable team rows with work item key, title, owner, status, and remaining hours.
- [ ] **P1** Add expandable risk items with severity, team, epic, explanation, owner, and action or dependency context.
- [ ] **P1** Add epic progress rows with item count, remaining hours, and completion percentage.
- [ ] **P1** Allow selecting an epic from the epic progress view to update the epic filter.
- [ ] **P1** Add `aria-expanded` to every expandable control and preserve keyboard activation.
- [ ] **P1** Add a clear empty-state message when filters produce no matching work items.

### 2.4 Balanced MVP Integration

- [ ] **P1** Connect all dashboard sections to one filtered data flow rather than section-specific copies of the dataset.
- [ ] **P1** Ensure filters update issue counts, KPI calculations, team rows, effort chart, risk context, and epic progress together.
- [ ] **P1** Ensure the UI never mutates the source mock dataset.
- [ ] **P1** Add loading, empty, and invalid-data fallback states appropriate for local mock data.
- [ ] **P1** Verify the default state presents all four KPI cards, three teams, nine work items, risks, and epics in one coherent overview.

### 2.5 Visual Polish and Responsiveness

- [ ] **P2** Apply the specified warm off-white, teal, amber, and coral visual system.
- [ ] **P2** Establish typography roles for serif display headings and sans-serif operational labels.
- [ ] **P2** Use restrained borders, compact cards, and consistent spacing without nested card clutter.
- [ ] **P2** Add visible text labels alongside RAG colors for accessible risk communication.
- [ ] **P2** Implement desktop layout with one-row KPI cards and main content beside risk and epic content.
- [ ] **P2** Implement tablet layout with wrapped KPIs and stacked dashboard columns.
- [ ] **P2** Implement mobile layout with stacked cards and readable expandable details without horizontal page overflow.
- [ ] **P2** Check focus states, contrast, control sizing, and layout stability as values change.

**Phase 2 exit criteria:** The local dashboard presents a complete, filtered, expandable current-sprint executive overview from dedicated mock data.

## Phase 3: Integration

**Phase outcome:** Mock data is integrated through a replaceable data boundary without introducing live Jira dependencies.

- [ ] **P1** Define a `SprintDataProvider` or equivalent interface for retrieving sprint and work item data.
- [ ] **P1** Implement a local mock provider that returns the dedicated sprint dataset.
- [ ] **P1** Move data loading behind the provider boundary so UI components do not import raw records directly.
- [ ] **P1** Define the provider response shape for loading, success, empty, and error states.
- [ ] **P1** Add a deterministic mock refresh path so repeated runs produce the same dashboard state.
- [ ] **P1** Add fixture data for full, filtered, empty, blocked, and mixed-risk scenarios.
- [ ] **P2** Document the future Jira adapter boundary without implementing network calls or credentials.
- [ ] **P2** Verify that swapping the mock provider does not require changing KPI, filter, or presentation components.

**Phase 3 exit criteria:** The dashboard runs entirely on a documented mock provider and the UI is decoupled from the raw data source.

## Phase 4: Testing

**Phase outcome:** The dashboard is validated through unit, component, integration, accessibility, responsive, and end-to-end checks.

### 4.1 Unit Tests

- [ ] **P0** Test completed-hours, remaining-hours, total-hours, and completion-percentage calculations.
- [ ] **P0** Test status aggregation for To Do, In Progress, and Done.
- [ ] **P0** Test team aggregation and per-team completion calculations.
- [ ] **P0** Test red-over-amber-over-green risk precedence.
- [ ] **P0** Test empty datasets and zero-denominator calculations.
- [ ] **P0** Test filter predicates for team, sprint, epic, and owner.

### 4.2 Component and Integration Tests

- [ ] **P1** Test that the default dashboard renders all KPI cards, teams, risks, and epics.
- [ ] **P1** Test that changing each filter updates visible work item counts and derived metrics.
- [ ] **P1** Test team expansion and collapse behavior.
- [ ] **P1** Test risk expansion and collapse behavior.
- [ ] **P1** Test epic selection updates the epic filter and visible results.
- [ ] **P1** Test empty filtered results render an intentional empty state.
- [ ] **P1** Test the UI consumes the mock provider rather than importing raw data directly.

### 4.3 Accessibility and Responsive Checks

- [ ] **P1** Test semantic headings, labels, buttons, and form controls.
- [ ] **P1** Test `aria-expanded` values before and after each expandable interaction.
- [ ] **P1** Test keyboard access to filters and expandable controls.
- [ ] **P1** Run an automated accessibility scan and resolve actionable violations.
- [ ] **P1** Verify readable contrast for body text, controls, and risk labels.
- [ ] **P1** Verify desktop, tablet, and mobile layouts at representative viewport sizes.
- [ ] **P1** Verify no horizontal page overflow on mobile.

### 4.4 End-to-End and Build Checks

- [ ] **P0** Run the production build in CI or the documented local command.
- [ ] **P1** Run a browser smoke test from page load through filtering and expansion.
- [ ] **P1** Verify the local URL loads without Jira credentials or network access.
- [ ] **P1** Verify all functional acceptance criteria from `project_spec.md`.
- [ ] **P2** Capture a representative desktop and mobile screenshot for regression review.

**Phase 4 exit criteria:** The build passes, core data logic is covered, major interactions are tested, accessibility checks are clean or documented, and responsive behavior is verified.

## Phase 5: Documentation

**Phase outcome:** Developers can maintain the dashboard and stakeholders can use and interpret it correctly.

### 5.1 Developer Documentation

- [ ] **P1** Document prerequisites, supported Node.js/npm versions, installation, development, build, lint, and test commands.
- [ ] **P1** Document the source tree and ownership of data, selectors, components, styles, and tests.
- [ ] **P1** Document the sprint and work item data contract with valid field values.
- [ ] **P1** Document metric formulas for completion, status effort, team risk, aggregate risk, and scope change.
- [ ] **P1** Document the mock provider interface and how a future Jira adapter would replace it.
- [ ] **P1** Document local troubleshooting for empty data, failed builds, and occupied development ports.
- [ ] **P2** Add contribution guidance for adding teams, epics, owners, statuses, and test fixtures.

### 5.2 User Documentation

- [ ] **P1** Explain the purpose of the executive overview and the questions it is designed to answer.
- [ ] **P1** Explain each KPI and how completion and scope change are calculated.
- [ ] **P1** Explain Green, Amber, and Red risk states in words and with examples.
- [ ] **P1** Explain how to use team, sprint, epic, and owner filters.
- [ ] **P1** Explain how to expand team, risk, and epic details.
- [ ] **P1** Explain how to interpret effort by status and expected completion date.
- [ ] **P2** Add a short accessibility note describing text labels, keyboard use, and responsive behavior.
- [ ] **P2** Add a known limitations section covering mock data, current-sprint-only scope, and lack of live Jira integration.

### 5.3 Documentation Verification

- [ ] **P1** Cross-check developer documentation commands against the current `package.json` scripts.
- [ ] **P1** Cross-check user documentation terminology against the rendered dashboard.
- [ ] **P2** Add links from the project README to the developer and user documentation.

**Phase 5 exit criteria:** A developer can set up and extend the project, and a stakeholder can interpret the dashboard without needing implementation knowledge.

## Final Definition of Done

- [ ] All P0 tasks are complete.
- [ ] All phase exit criteria are met.
- [ ] The dashboard runs locally from a clean install.
- [ ] The production build succeeds.
- [ ] Core calculations, filters, expansions, provider integration, accessibility, and responsive behavior are tested.
- [ ] Developer and user documentation are complete and consistent with the implementation.
- [ ] No live Jira credentials, API calls, or unrelated root-level automation files are introduced.
