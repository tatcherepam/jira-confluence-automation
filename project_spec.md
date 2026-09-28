# Jira Sprint Dashboard Technical Specification

## 1. Document Control

| Field | Value |
| --- | --- |
| Project | Atlas Program Delivery Intelligence |
| Version | 1.0 |
| Status | Initial prototype specification |
| Audience | Leadership and project stakeholders |
| Implementation | React with Vite |
| Data source | Dedicated local mock dataset |
| Current application directory | `jira-dashboard/` |

## 2. Objective

Build a React dashboard that gives leadership a concise, decision-oriented view of the current program sprint. The dashboard must surface overall progress, expected completion, scope change, team comparison, epic delivery, and delivery risks without requiring users to open Jira.

The initial release is a local prototype. It must use dedicated mock data and must not require Jira credentials or network access to display its core experience.

## 3. Scope

### 3.1 In scope

- One program containing three teams: Team Alpha, Team Beta, and Team Gamma.
- One active two-week sprint.
- Current sprint view only.
- Progress calculated from estimated and remaining hours.
- Standard work statuses: To Do, In Progress, and Done.
- Aggregate program progress and team-level comparison.
- Filters for team, sprint, epic, and owner.
- Expandable team, epic, and risk details shown inline.
- Expected completion date forecast.
- Scope-change and delivery-risk indicators.
- RAG risk communication using green, amber, and red states.
- Responsive desktop and mobile layouts.

### 3.2 Out of scope

- Live Jira API integration.
- Jira authentication, OAuth, or API token management.
- Historical sprint trend analysis.
- Completion probability calculations.
- Jira issue editing or workflow transitions.
- Separate team or risk detail pages.
- Changes to existing Python scripts or `jira_data.json`.

## 4. User Experience Requirements

### 4.1 Executive overview

The first viewport must answer these questions quickly:

1. How much of the sprint is complete?
2. When is the work expected to finish?
3. Has the sprint scope changed?
4. Is delivery at risk?
5. Which team or dependency needs attention?

The layout must use a balanced visual language: polished and spacious enough for leadership, with practical Jira-style detail for investigation.

### 4.2 Page structure

The page must render these sections in order:

1. Program identity and data freshness context.
2. Current sprint heading and date context.
3. Team, sprint, epic, and owner filters.
4. Headline KPI row.
5. Team progress comparison.
6. Effort by status.
7. Risks and focus areas.
8. Epic progress.

### 4.3 Headline KPIs

The KPI row must include:

| KPI | Required behavior |
| --- | --- |
| Overall completion | Show completed effort divided by total estimated effort as a percentage. |
| Expected finish | Show a concrete expected completion date. |
| Scope change | Show the percentage and hour impact of scope added or removed since sprint start. |
| Delivery risk | Show the aggregate RAG state and supporting counts or context. |

KPI values must update when team, epic, or owner filters are applied, except for sprint-level context that intentionally remains global.

### 4.4 Team comparison

Each team row must show:

- Team name.
- Number of work items.
- Total estimated hours.
- Completion percentage.
- Remaining hours.
- RAG state with a text label.
- Expand/collapse control.

Expanded team detail must show work item key, title, owner, status, and remaining hours.

### 4.5 Risk and focus areas

The dashboard must show the highest-priority delivery concerns. Each focus item must provide:

- A visible risk severity indicator.
- Short issue title.
- Team and epic context.
- Expandable explanation.
- Owner or responsible role.
- Action, dependency, or decision context where available.

RAG color must be supplemented by text so the state is understandable without color perception.

### 4.6 Filters

Filters must be implemented as native select controls or equivalent accessible controls.

| Filter | Values |
| --- | --- |
| Team | All teams, Team Alpha, Team Beta, Team Gamma |
| Sprint | Active sprint and future-compatible sprint values |
| Epic | Values derived from the dataset |
| Owner | Values derived from the dataset |

Applying filters must update visible issue counts, KPI calculations, team rows, effort chart, risk context, and epic progress.

## 5. Technical Architecture

### 5.1 Application structure

The prototype must remain isolated in the `jira-dashboard/` directory.

Recommended structure:

```text
jira-dashboard/
  package.json
  index.html
  src/
    main.jsx
    App.jsx
    App.css
    index.css
    data/
      sprintData.js
    components/
      Header.jsx
      Filters.jsx
      KpiGrid.jsx
      TeamProgress.jsx
      RiskPanel.jsx
      EpicProgress.jsx
```

The current prototype may keep components in `App.jsx` during initial development, but the data and UI boundaries should remain separable for future refactoring.

### 5.2 State management

Local React state is sufficient for the prototype.

Required state:

- Selected team.
- Selected sprint.
- Selected epic.
- Selected owner.
- Expanded section or item.

Derived values must be calculated from the filtered dataset rather than duplicated in state.

### 5.3 Data flow

```text
Mock dataset
    -> active filter state
    -> filtered work items
    -> derived metrics
    -> KPI, team, risk, status, and epic views
```

The presentation layer must not mutate the source dataset directly.

## 6. Data Contract

### 6.1 Sprint object

```js
{
  id: "sprint-24",
  name: "Sprint 24",
  program: "Atlas",
  startDate: "2026-09-16",
  endDate: "2026-09-27",
  expectedCompletionDate: "2026-09-30",
  scopeChangeHours: 14,
  status: "active"
}
```

### 6.2 Work item object

```js
{
  key: "ATL-153",
  title: "Invoice export v2",
  team: "Team Alpha",
  epic: "Finance tools",
  owner: "Maya Chen",
  sprintId: "sprint-24",
  status: "To Do",
  estimateHours: 14,
  remainingHours: 14,
  risk: "red",
  blocker: "Waiting on finance schema approval"
}
```

### 6.3 Allowed values

- `status`: `To Do`, `In Progress`, `Done`
- `risk`: `green`, `amber`, `red`
- `sprint.status`: `active`

The dataset must contain enough variation to demonstrate all statuses, all RAG levels, multiple epics, multiple owners, and at least one blocker or dependency.

## 7. Metric Definitions

### 7.1 Completion

```text
totalEstimatedHours = sum(estimateHours)
remainingHours = sum(remainingHours)
completedHours = totalEstimatedHours - remainingHours
completionPercent = round(completedHours / totalEstimatedHours * 100)
```

When no work items match the current filters, display zero values and an explicit empty-state message instead of producing `NaN`.

### 7.2 Status effort

For each allowed status, sum `estimateHours` for matching work items. Display the result as hours in the effort-by-status visualization.

### 7.3 Team risk

For a team:

1. Return `red` if any matching work item is red.
2. Otherwise return `amber` if any matching work item is amber.
3. Otherwise return `green`.

### 7.4 Aggregate risk

The executive risk state uses the same precedence rule across all visible work items. The UI must also show the number of high and medium concerns where those values are available.

## 8. Accessibility and Responsive Behavior

- Use semantic headings, sections, articles, buttons, labels, and form controls.
- Every expandable control must expose `aria-expanded`.
- Every filter must have an accessible label.
- Do not communicate state through color alone.
- Preserve readable contrast for text and status labels.
- Support keyboard activation of expandable rows and filters.
- At desktop widths, show KPI cards in one row and the main content beside the risk/epic column.
- At tablet widths, allow KPI cards to wrap and stack the main content columns.
- At mobile widths, stack KPI cards and dashboard columns; keep team details readable without horizontal page overflow.

## 9. Visual Design Direction

- Use a warm off-white canvas with a restrained teal primary color.
- Use coral for high-risk emphasis and amber for watch states.
- Use a serif display face for major headings and a clear sans-serif for operational labels.
- Use subtle borders, compact cards, and quiet background contrast rather than heavy decoration.
- Avoid purple-dominant palettes, dark-mode-only styling, and dense nested cards.
- Keep controls and labels stable so content changes do not cause layout shifts.

## 10. Performance and Maintainability

- No backend or network request is required for the prototype.
- Keep the initial bundle small and use only the React dependencies needed by the app.
- Keep mock data separate from derived metric logic where practical.
- Avoid duplicating metric calculations in individual components.
- Keep existing root-level Python automation files unchanged.

## 11. Verification Plan

### 11.1 Build validation

Run from `jira-dashboard/`:

```powershell
npm.cmd run build
```

The command must complete successfully and create a production build.

### 11.2 Local run

```powershell
npm.cmd run dev
```

The application must be available at `http://localhost:5173/` unless the port is already occupied.

### 11.3 Functional checks

- The page loads with all four KPI cards visible.
- The default view shows all three teams and nine mock work items.
- Team, epic, and owner filters change the visible counts and metrics.
- Team rows expand and collapse inline.
- Risk items expand and collapse inline.
- Epic selections update the epic filter and visible dataset.
- Empty filtered results do not break the page.
- The dashboard remains usable at mobile width.

## 12. Acceptance Criteria

The implementation is accepted when:

1. Leadership can identify overall sprint health within the first viewport.
2. The KPI row includes completion, expected finish date, scope change, and RAG risk.
3. Team Alpha, Team Beta, and Team Gamma can be compared clearly.
4. Progress is based on hours or remaining effort.
5. Only the specified standard workflow statuses appear.
6. Team, sprint, epic, and owner filters are available and functional.
7. Team, epic, and risk details expand inline.
8. The UI is responsive and keyboard-usable.
9. The prototype runs locally without Jira credentials.
10. Existing non-dashboard workspace files remain unaffected.