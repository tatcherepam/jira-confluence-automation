# Jira Sprint Dashboard Requirements

## 1. Purpose

Build a React dashboard that gives leadership and stakeholders a concise view of the current program sprint, including delivery progress, forecast, team comparison, and risks.

The first version will use dedicated mock data for design and validation. It will not connect to Jira yet.

## 2. Audience

Primary users are leadership and project stakeholders.

The experience should support fast executive scanning while allowing users to inspect the details behind progress and risk signals.

## 3. Scope

### In scope

- Several teams within one program
- Three sample teams:
  - Team Alpha
  - Team Beta
  - Team Gamma
- Current sprint only
- Two-week sprint cadence
- Comparison of team progress and aggregate program progress
- Dedicated mock dataset optimized for this dashboard
- Responsive React interface

### Out of scope for the first version

- Live Jira API integration
- Jira authentication and credentials
- Historical sprint trend charts
- Replacing Jira as a work-management system

## 4. Primary dashboard experience

The initial view should use a balanced executive layout:

1. Headline KPI row
2. Team comparison
3. Sprint progress and forecast details
4. Expandable epic and risk details

The surface should feel polished and presentation-ready while retaining practical Jira-style detail.

## 5. Headline KPIs

The KPI row must show:

- Overall sprint completion
- Expected completion date, for example `Likely to finish Sep 30`
- Scope change
- Overall delivery risk using RAG status

Forecast should be expressed primarily as an expected completion date. The first version does not need a completion probability or committed-versus-forecast effort KPI.

## 6. Progress model

- Estimate progress using hours or remaining effort.
- Use the standard Jira workflow:
  - To Do
  - In Progress
  - Done
- Show aggregate program progress and progress by team.
- Make the relationship between completed effort and total effort clear.

## 7. Filters

Provide filters for:

- Team
- Sprint
- Epic
- Owner

Filters should update the visible dashboard data without making the executive overview feel cluttered.

## 8. Team comparison

Show Team Alpha, Team Beta, and Team Gamma in a compact comparison view. Each team should expose enough information to compare:

- Completion percentage
- Completed and remaining effort
- Expected delivery status or forecast
- RAG risk status

The comparison should also support the aggregate program view.

## 9. Expandable detail sections

Use expandable sections to reveal details inline rather than navigating to separate pages.

Expandable content should include:

- Team details
- Epic details
- Risk details

Risk details should make the underlying issue, owner, and relevant action or dependency understandable.

## 10. Risk communication

Use RAG indicators:

- Green: on track
- Amber: needs attention or has moderate delivery risk
- Red: at risk or blocked

RAG status should be visible at the overall and team levels, with supporting details available in the expandable risk section. The color system must not be the only way risk is communicated; include text labels or supporting context for accessibility and clarity.

## 11. Mock data requirements

Create a dedicated mock dataset rather than adapting the existing `jira_data.json` file.

The dataset should be rich enough to demonstrate:

- Three teams in one program
- A two-week current sprint
- Multiple epics
- Owners
- Issues in To Do, In Progress, and Done states
- Hour-based estimates and remaining effort
- Completed and remaining work
- Scope additions or removals
- Expected completion dates
- Green, amber, and red risk states
- At least one meaningful blocker or dependency

The existing workspace Jira data and Python reporting scripts should remain unchanged.

## 12. Technical requirements

- Implement the prototype in React.
- Use a component-based structure so future interactions and Jira integration can be added cleanly.
- Keep mock data separate from presentation components.
- Use responsive layout behavior for desktop and smaller screens.
- Keep the first implementation self-contained in a new dashboard project within the workspace.

## 13. Future considerations

The design should leave room for a later phase that adds:

- Live Jira data retrieval
- Authentication and API configuration
- Historical sprint comparisons
- More teams or programs
- More detailed forecasting, such as completion probability and committed-versus-forecast effort

## 14. Acceptance criteria

The first prototype is complete when:

- Leadership can identify overall sprint health at a glance.
- The KPI row shows completion, expected completion date, scope change, and RAG risk.
- The three teams can be compared without excessive visual density.
- Team, sprint, epic, and owner filters work with the mock data.
- Team, epic, and risk details expand inline.
- Progress is based on hours or remaining effort.
- Only To Do, In Progress, and Done are used as workflow statuses.
- The interface works on desktop and mobile-sized screens.
- Existing workspace files outside the new dashboard project are unaffected.