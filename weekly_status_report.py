import argparse
import json
from pathlib import Path


def load_issues(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("issues", data)


def status_key(issue):
    return str(issue.get("status", "")).strip().lower()


def render_report(issues):
    completed = [issue for issue in issues if status_key(issue) in {"done", "closed", "resolved", "completed"}]
    in_progress = [issue for issue in issues if status_key(issue) in {"in progress", "in-progress", "review", "testing", "code review"}]
    blockers = [issue for issue in issues if status_key(issue) in {"blocked", "waiting", "blocked by dependency"} or issue.get("blocked_by")]

    lines = [
        "## Weekly Engineering Status Report",
        "",
        "### Completed issues",
    ]
    if completed:
        for issue in completed:
            lines.append(f"- {issue.get('key', 'N/A')} — {issue.get('summary', 'No summary')} ({issue.get('assignee', 'Unassigned')})")
    else:
        lines.append("- No completed issues this week")

    lines.extend(["", "### In-progress items"]) 
    if in_progress:
        for issue in in_progress:
            lines.append(f"- {issue.get('key', 'N/A')} — {issue.get('summary', 'No summary')} [{issue.get('status', 'Unknown')}]")
    else:
        lines.append("- No in-progress items")

    lines.extend(["", "### Blockers"]) 
    if blockers:
        for issue in blockers:
            reason = issue.get("blocked_by") or issue.get("risk") or "Awaiting dependency"
            lines.append(f"- {issue.get('key', 'N/A')} — {issue.get('summary', 'No summary')} | {reason}")
    else:
        lines.append("- No active blockers")

    lines.extend(["", "### Next sprint goals"]) 
    goals = []
    for issue in issues:
        if issue.get("priority") in {"High", "Critical"}:
            goals.append(f"- Finish {issue.get('key', 'N/A')} — {issue.get('summary', 'No summary')}")
    if not goals:
        goals = [
            "- Finish current sprint scope and close remaining defects",
            "- Resolve remaining dependencies before sprint end",
            "- Confirm delivery readiness for the next release",
        ]
    lines.extend(goals)
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate weekly engineering status report from Jira-like JSON data.")
    parser.add_argument("input", nargs="?", default="jira_data.json", help="Path to JSON file containing issue data")
    parser.add_argument("output", nargs="?", default="weekly_status_report.md", help="Path to save the markdown report")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    issues = load_issues(input_path)
    report = render_report(issues)
    output_path.write_text(report, encoding="utf-8")
    print(f"Weekly report written to {output_path}")


if __name__ == "__main__":
    main()
