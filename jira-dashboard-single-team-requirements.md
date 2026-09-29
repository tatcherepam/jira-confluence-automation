# Single-Team Jira Leadership Dashboard Technical Specification

## 1. Document Control

| Field | Value |
| --- | --- |
| Project | Atlas Team Alpha Leadership Dashboard |
| Version | 1.0 |
| Status | Initial prototype specification |
| Audience | Leadership only |
| Implementation | React with Vite |
| Data source | Dedicated local mock dataset |
| Application directory | `jira-dashboard/` |

## 2. Objective

Build a React dashboard that gives leadership a concise, decision-oriented view of Team Alpha's current sprint. The dashboard must surface delivery progress, expected completion, scope change, epic health, blockers, risks, and decisions requiring leadership attention.

The initial release is a local prototype. It must use dedicated mock data and must not require Jira credentials, network access, or live Jira integration to display its core experience.

## 3. Scope and Non-Goals

### 3.1 In scope

- One fixed team: Team Alpha.
- One active two-week sprint.
- Current sprint view only.
- Progress based on estimated and remaining hours.
- Standard statuses: To Do, In Progress, and Done.
- Executive KPI row for completion, effort, forecast, scope, risk, and blockers.
- Epic and milestone progress.
- Sprint, epic, and owner filters.
- Expandable epic, risk, blocker, decision, and key work item details.
- Green, amber, and red risk communication with text labels.
- Dedicated mock dataset.
- Responsive desktop, tablet, and mobile layouts.

### 3.2 Non-goals

- Multiple teams or team comparison.
- Team selection or a team filter.
- Live Jira API calls.
- Jira authentication, OAuth, or API token management.
- Historical sprint trend analysis.
- Individual performance ranking.
- Issue editing or workflow transitions.
- Separate team or risk pages.
- Replacing Jira as a work-management system.
- Changes to existing Python scripts or `jira_data.json`.

## 4. User Experience Requirements

### 4.1 Leadership overview

The first viewport must answer these questions quickly:

1. Is Team Alpha's sprint on track?
2. When is the work expected to finish?
3. How much effort is complete and how much remains?
4. Has scope changed materially?
5. Which epic or milestone is most at risk?
6. What blocker or decision requires leadership attention?

The surface must prioritize summary, delivery confidence, and decisions over a complete operational issue inventory.

### 4.2 Page structure

Render sections in this order:

1. Team identity, sprint identity, and data freshness context.
2. Headline KPI row.
3. Sprint progress and expected finish.
4. Epic and milestone health.
5. Risks, blockers, and decisions needed.
6. Expandable supporting details.

Use a polished, presentation-ready visual style with restrained Jira-style detail.

### 4.3 Headline KPIs

The KPI row must show:

| KPI | Required behavior |
| --- | --- |
| Completion | Display completed effort divided by total estimated effort as a percentage. |
| Effort | Display completed and remaining effort in hours. |
| Expected finish | Display the concrete expected completion date. |
| Scope change | Display added or removed hours and the percentage change since sprint start. |
| Delivery risk | Display aggregate RAG state with text and supporting context. |
| Blockers | Display the count of active blockers requiring attention. |

Forecast is expressed primarily as an expected completion date, for example `Likely to finish Sep 30`. Completion probability is not required for this version.

### 4.4 Filters

Provide only filters that support leadership investigation:

| Filter | Values |
| --- | --- |
| Sprint | Active sprint and future-compatible sprint values |
| Epic | Values derived from the dataset |
| Owner | Values derived from the dataset |

Do not provide a team filter because this dashboard represents one fixed team.

Applying filters must update visible item counts, KPI calculations, effort-by-status values, epic progress, and risk context without changing the fixed Team Alpha identity.

### 4.5 Epic and milestone progress

Each epic or milestone row must show:

- Epic name.
- Business or delivery outcome.
- Completion percentage.
- Completed and remaining hours.
- Expected delivery state.
- RAG risk state with text label.
- Key dependency when applicable.

Expanded epic details must show the key work items contributing to the outcome.

### 4.6 Risks, blockers, and decisions

Each risk or blocker must show:

- Title and severity.
- Impact on sprint or business outcome.
- Team context, fixed as Team Alpha.
- Owner or responsible role.
- Dependency or cause.
- Mitigation or next action.
- Decision deadline when applicable.
- Consequence of delay when applicable.

RAG colors must always be accompanied by text labels and supporting context.

## 5. Technical Architecture

### 5.1 Application structure

Keep the prototype isolated in `jira-dashboard/`.

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
      SprintProgress.jsx
      EpicProgress.jsx
      RiskPanel.jsx
```

The first prototype may keep components in `App.jsx`, but data, derived metrics, and presentation responsibilities must remain separable for future refactoring.

### 5.2 State management

Local React state is sufficient.

Required state:

- Selected sprint.
- Selected epic.
- Selected owner.
- Expanded section or item.

Team identity is static and must not be stored as a user-selectable filter.

Derived values must be calculated from filtered work items rather than duplicated in state.

### 5.3 Data flow

```text
Mock dataset
    -> sprint, epic, and owner filter state
    -> filtered Team Alpha work items
    -> derived metrics
    -> KPI, progress, epic, risk, and detail views
```

Presentation components must not mutate the source dataset directly.

## 6. Data Contract

### 6.1 Sprint object

```js
{
  id: "sprint-24",
  name: "Sprint 24",
  program: "Atlas",
  team: "Team Alpha",
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
  blocker: "Waiting on finance schema approval",
  decisionNeeded: "Approve the finance schema",
  decisionDueDate: "2026-09-29"
}
```

### 6.3 Allowed values

- `team`: `Team Alpha`
- `status`: `To Do`, `In Progress`, `Done`
- `risk`: `green`, `amber`, `red`
- `sprint.status`: `active`

The dataset must include multiple epics and owners, all statuses, all RAG states, at least one blocker, and at least one leadership decision or approval requirement.

## 7. Metric and Behavior Definitions

### 7.1 Completion and effort

```text
totalEstimatedHours = sum(estimateHours)
remainingHours = sum(remainingHours)
completedHours = totalEstimatedHours - remainingHours
completionPercent = round(completedHours / totalEstimatedHours * 100)
```

When no items match the selected filters, return zero values and show an explicit empty state instead of producing `NaN` or misleading totals.

### 7.2 Effort by status

For each allowed status, sum `estimateHours` for matching work items. Display the result as hours for To Do, In Progress, and Done.

### 7.3 Risk precedence

For the visible filtered work items:

1. Return `red` if any item is red.
2. Otherwise return `amber` if any item is amber.
3. Otherwise return `green`.

Display the risk state with a text label and supporting count or explanation.

### 7.4 Scope change

```text
scopeChangePercent = round(scopeChangeHours / initialCommittedHours * 100)
```

Show whether scope was added or removed. If the initial committed value is unavailable, display the hours and mark the percentage as unavailable rather than inventing a denominator.

### 7.5 Expected finish

Display the sprint's `expectedCompletionDate` as the primary forecast. The dashboard must make it clear that this is a forecast based on the current mock throughput and dependencies.

## 8. Accessibility and Responsive Behavior

- Use semantic headings, sections, articles, buttons, labels, and form controls.
- Give every filter an accessible label.
- Give every expandable control an `aria-expanded` attribute.
- Support keyboard activation for filters and expandable controls.
- Do not communicate risk through color alone.
- Preserve readable contrast for text, controls, and RAG labels.
- At desktop widths, show the KPI row above progress and risk content.
- At tablet widths, allow KPI cards to wrap and content columns to stack.
- At mobile widths, stack cards and details without horizontal page overflow.
- Keep labels and values readable when filters change the amount of content.

## 9. Performance and Maintainability

- No backend or network request is required for the prototype.
- Keep the initial bundle small and use only necessary dependencies.
- Keep mock data separate from metric selectors and presentation components.
- Avoid duplicate calculations across UI components.
- Preserve a future data-provider boundary for later Jira integration.
- Keep existing root-level Python automation files unchanged.

## 10. Verification Plan

### 10.1 Build and local run

Run from `jira-dashboard/`:

```powershell
npm.cmd run build
npm.cmd run dev
```

The application must load at `http://localhost:5173/` unless the port is occupied.

### 10.2 Functional checks

- The default view identifies Team Alpha and the active sprint.
- All six KPI values are visible and derived from the mock data.
- Sprint, epic, and owner filters update the visible metrics and details.
- No team comparison or team filter appears.
- Epic rows expand and collapse inline.
- Risk and blocker rows expand and collapse inline.
- Leadership decision deadlines and consequences are visible.
- Empty filtered results show an intentional empty state.
- The app works at desktop, tablet, and mobile viewport sizes.

### 10.3 Acceptance validation

Verify each acceptance criterion in Section 11 manually or with automated tests. Confirm that existing files outside the dashboard project are unchanged.

## 11. Acceptance Criteria

The first prototype is complete when:

1. Leadership can identify Team Alpha's overall sprint health at a glance.
2. The KPI row shows completion, completed and remaining hours, expected completion date, scope change, RAG risk, and blocker count.
3. The dashboard represents one team only and has no team comparison controls.
4. Sprint, epic, and owner filters work with the mock data.
5. Epic, risk, blocker, and key work item details expand inline.
6. Progress is based on hours or remaining effort.
7. Only To Do, In Progress, and Done appear as workflow statuses.
8. Green, Amber, and Red states include text explanations.
9. Leadership decisions, owners, due dates, and consequences of delay are visible.
10. The interface works on desktop and mobile-sized screens.
11. The production build succeeds and the local app runs without Jira credentials.
12. Existing workspace files outside the new dashboard project are unaffected.