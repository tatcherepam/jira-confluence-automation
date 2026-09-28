import { useMemo, useState } from 'react'
import './App.css'

const sprint = { name: 'Sprint 24 · Atlas release', dates: 'Sep 16 - Sep 27, 2026', daysLeft: 3, expectedDate: 'Sep 30, 2026' }

const issues = [
  { key: 'ATL-142', title: 'Checkout recovery flow', team: 'Team Alpha', epic: 'Customer trust', owner: 'Maya Chen', status: 'Done', estimate: 18, remaining: 0, risk: 'green' },
  { key: 'ATL-149', title: 'Saved payment methods', team: 'Team Alpha', epic: 'Customer trust', owner: 'Jon Bell', status: 'In Progress', estimate: 24, remaining: 8, risk: 'amber' },
  { key: 'ATL-153', title: 'Invoice export v2', team: 'Team Alpha', epic: 'Finance tools', owner: 'Maya Chen', status: 'To Do', estimate: 14, remaining: 14, risk: 'red', blocker: 'Waiting on finance schema approval' },
  { key: 'ATL-161', title: 'Device trust signals', team: 'Team Beta', epic: 'Identity platform', owner: 'Priya Shah', status: 'Done', estimate: 20, remaining: 0, risk: 'green' },
  { key: 'ATL-166', title: 'Session risk scoring', team: 'Team Beta', epic: 'Identity platform', owner: 'Owen Wright', status: 'In Progress', estimate: 22, remaining: 7, risk: 'green' },
  { key: 'ATL-171', title: 'Account recovery audit', team: 'Team Beta', epic: 'Customer trust', owner: 'Priya Shah', status: 'In Progress', estimate: 16, remaining: 10, risk: 'amber', blocker: 'Security review scheduled Sep 29' },
  { key: 'ATL-180', title: 'Usage insights dashboard', team: 'Team Gamma', epic: 'Growth insights', owner: 'Luis Park', status: 'Done', estimate: 26, remaining: 0, risk: 'green' },
  { key: 'ATL-184', title: 'Activation funnel events', team: 'Team Gamma', epic: 'Growth insights', owner: 'Luis Park', status: 'In Progress', estimate: 18, remaining: 6, risk: 'green' },
  { key: 'ATL-188', title: 'Segment export permissions', team: 'Team Gamma', epic: 'Finance tools', owner: 'Sara Kim', status: 'To Do', estimate: 12, remaining: 12, risk: 'amber' },
]

const teams = ['All teams', 'Team Alpha', 'Team Beta', 'Team Gamma']
const statuses = ['To Do', 'In Progress', 'Done']
const hours = (value) => `${value}h`

function RiskPill({ level, label = level }) {
  return <span className={`risk-pill ${level}`}><span className="risk-dot" />{label}</span>
}

function App() {
  const [team, setTeam] = useState('All teams')
  const [epic, setEpic] = useState('All epics')
  const [owner, setOwner] = useState('All owners')
  const [expanded, setExpanded] = useState('teams')
  const epics = ['All epics', ...new Set(issues.map((issue) => issue.epic))]
  const owners = ['All owners', ...new Set(issues.map((issue) => issue.owner))]
  const filteredIssues = useMemo(() => issues.filter((issue) => (team === 'All teams' || issue.team === team) && (epic === 'All epics' || issue.epic === epic) && (owner === 'All owners' || issue.owner === owner)), [team, epic, owner])
  const totalHours = filteredIssues.reduce((sum, issue) => sum + issue.estimate, 0)
  const remainingHours = filteredIssues.reduce((sum, issue) => sum + issue.remaining, 0)
  const completedHours = totalHours - remainingHours
  const completion = totalHours ? Math.round((completedHours / totalHours) * 100) : 0
  const blockedIssues = filteredIssues.filter((issue) => issue.blocker)
  const teamRows = teams.slice(1).map((name) => {
    const teamIssues = filteredIssues.filter((issue) => issue.team === name)
    const total = teamIssues.reduce((sum, issue) => sum + issue.estimate, 0)
    const remaining = teamIssues.reduce((sum, issue) => sum + issue.remaining, 0)
    const risk = teamIssues.some((issue) => issue.risk === 'red') ? 'red' : teamIssues.some((issue) => issue.risk === 'amber') ? 'amber' : 'green'
    return { name, total, remaining, completion: total ? Math.round(((total - remaining) / total) * 100) : 0, risk, issues: teamIssues }
  })
  const toggle = (section) => setExpanded((current) => current === section ? '' : section)

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-lockup"><div className="brand-mark">A</div><div><strong>Atlas program</strong><span>Delivery intelligence</span></div></div>
        <div className="topbar-meta"><span className="live-dot" /> Mock data <span className="divider" /> Last refreshed 9:42 AM</div>
        <button className="avatar" aria-label="Open profile">TC</button>
      </header>

      <section className="page-heading">
        <div><p className="eyebrow">Program pulse <span>·</span> Current sprint</p><h1>Make the next move visible.</h1><p className="lede">A clear view of delivery momentum across the Atlas teams, with the decisions that need attention close at hand.</p></div>
        <div className="sprint-context"><span className="context-label">Active sprint</span><strong>{sprint.name}</strong><span>{sprint.dates} <b>·</b> {sprint.daysLeft} days left</span></div>
      </section>

      <section className="filters" aria-label="Dashboard filters">
        <div className="filter-label">View by</div>
        <label>Team<select value={team} onChange={(event) => setTeam(event.target.value)}>{teams.map((item) => <option key={item}>{item}</option>)}</select></label>
        <label>Epic<select value={epic} onChange={(event) => setEpic(event.target.value)}>{epics.map((item) => <option key={item}>{item}</option>)}</select></label>
        <label>Owner<select value={owner} onChange={(event) => setOwner(event.target.value)}>{owners.map((item) => <option key={item}>{item}</option>)}</select></label>
        <div className="filter-result">Showing <strong>{filteredIssues.length}</strong> work items</div>
      </section>

      <section className="kpi-grid" aria-label="Sprint KPIs">
        <article className="kpi-card accent-card"><div className="kpi-heading"><span>Overall completion</span><span className="trend up">+8%</span></div><strong className="kpi-value">{completion}%</strong><div className="meter"><span style={{ width: `${completion}%` }} /></div><small>{hours(completedHours)} of {hours(totalHours)} delivered</small></article>
        <article className="kpi-card"><div className="kpi-heading"><span>Expected finish</span><span className="kpi-icon">↗</span></div><strong className="kpi-value date">{sprint.expectedDate}</strong><small>Based on current throughput</small><div className="confidence"><span className="confidence-line" /> On track for sprint close</div></article>
        <article className="kpi-card"><div className="kpi-heading"><span>Scope change</span><span className="trend neutral">+12h</span></div><strong className="kpi-value">+9%</strong><small>14h added since sprint start</small><div className="scope-bars"><i /><i /><i /><i /><i /><i /><i /><i /></div></article>
        <article className="kpi-card risk-card"><div className="kpi-heading"><span>Delivery risk</span><RiskPill level="amber" label="Needs attention" /></div><strong className="kpi-value">Amber</strong><small>{blockedIssues.length || 2} active dependencies need a decision</small><div className="risk-summary"><span className="risk-count red-count">1</span> High <span className="risk-count amber-count">2</span> Medium</div></article>
      </section>

      <section className="dashboard-grid">
        <div className="main-column">
          <div className="section-heading"><div><p className="eyebrow">Program delivery</p><h2>Team progress</h2></div><span className="section-note">{hours(completedHours)} delivered of {hours(totalHours)}</span></div>
          <div className="team-list">{teamRows.map((row) => <article className="team-row" key={row.name}><button className="row-toggle" onClick={() => toggle(row.name)} aria-expanded={expanded === row.name}><span className="chevron">{expanded === row.name ? '⌄' : '›'}</span><span className="team-name"><strong>{row.name}</strong><small>{row.issues.length} work items · {hours(row.total)} total</small></span><div className="team-progress"><div className="team-progress-top"><span>{row.completion}% complete</span><span>{hours(row.remaining)} remaining</span></div><div className="meter"><span style={{ width: `${row.completion}%` }} /></div></div><RiskPill level={row.risk} label={row.risk === 'green' ? 'On track' : row.risk === 'amber' ? 'Watch' : 'At risk'} /></button>{expanded === row.name && <div className="team-detail"><div className="detail-header"><span>Work item</span><span>Owner</span><span>State</span><span>Effort</span></div>{row.issues.map((issue) => <div className="detail-row" key={issue.key}><span><b>{issue.key}</b> {issue.title}</span><span>{issue.owner}</span><span className={`state ${issue.status.toLowerCase().replace(' ', '-')}`}>{issue.status}</span><span>{hours(issue.remaining)} left</span></div>)}</div>}</article>)}</div>
          <div className="section-heading lower-heading"><div><p className="eyebrow">Delivery shape</p><h2>Effort by status</h2></div><span className="section-note">{filteredIssues.length} items in view</span></div>
          <div className="status-card"><div className="status-chart">{statuses.map((status) => { const statusHours = filteredIssues.filter((issue) => issue.status === status).reduce((sum, issue) => sum + issue.estimate, 0); return <div className="status-column" key={status}><div className={`column-bar ${status.toLowerCase().replace(' ', '-')}`} style={{ height: `${totalHours ? Math.max(18, (statusHours / totalHours) * 150) : 18}px` }}><span>{statusHours}h</span></div><small>{status}</small></div> })}</div><div className="status-insight"><span className="insight-kicker">Signal</span><strong>Momentum is healthy</strong><p>Most remaining effort is already in progress, giving the teams room to absorb the open dependency.</p></div></div>
        </div>

        <aside className="side-column">
          <div className="section-heading"><div><p className="eyebrow">Focus areas</p><h2>What needs attention</h2></div><span className="count-badge">{blockedIssues.length + 2}</span></div>
          <div className="attention-card"><button className="attention-item" onClick={() => toggle('risks')} aria-expanded={expanded === 'risks'}><span className="attention-icon red">!</span><span><strong>Invoice export is blocked</strong><small>Team Alpha · Finance tools</small></span><span className="chevron">{expanded === 'risks' ? '⌄' : '›'}</span></button>{expanded === 'risks' && <div className="attention-detail"><p>Finance schema approval is holding 14h of work. A decision by Sep 29 keeps the current forecast intact.</p><span className="owner-chip">Owner · Maya Chen</span></div>}<button className="attention-item" onClick={() => toggle('review')} aria-expanded={expanded === 'review'}><span className="attention-icon amber">↗</span><span><strong>Security review is upcoming</strong><small>Team Beta · Sep 29 checkpoint</small></span><span className="chevron">{expanded === 'review' ? '⌄' : '›'}</span></button>{expanded === 'review' && <div className="attention-detail"><p>Account recovery audit has 10h remaining. The review is the final gate before the item can move to Done.</p><span className="owner-chip">Owner · Priya Shah</span></div>}</div>
          <div className="section-heading epic-heading"><div><p className="eyebrow">Outcome map</p><h2>Epic progress</h2></div></div>
          <div className="epic-list">{[...new Set(filteredIssues.map((issue) => issue.epic))].map((epicName) => { const epicIssues = filteredIssues.filter((issue) => issue.epic === epicName); const total = epicIssues.reduce((sum, issue) => sum + issue.estimate, 0); const remaining = epicIssues.reduce((sum, issue) => sum + issue.remaining, 0); const percent = total ? Math.round(((total - remaining) / total) * 100) : 0; return <button className="epic-row" key={epicName} onClick={() => setEpic(epicName)}><span className="epic-mark">{epicName.slice(0, 1)}</span><span className="epic-info"><strong>{epicName}</strong><small>{epicIssues.length} items · {hours(remaining)} left</small></span><span className="epic-percent">{percent}%</span></button> })}</div>
        </aside>
      </section>
      <footer><span>Atlas delivery intelligence</span><span>Designed for decision velocity <b>·</b> Sprint 24</span></footer>
    </main>
  )
}

export default App