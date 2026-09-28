import argparse
import base64
import json
import os
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage
from pathlib import Path


def load_issues(path):
    if not path or not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("issues", data)


def fetch_jira_issues(base_url, email, api_token, project_key=None, jql=None):
    base_url = base_url.rstrip("/")
    if not jql:
        if project_key:
            jql = f'project = "{project_key}" ORDER BY updated DESC'
        else:
            jql = 'ORDER BY updated DESC'

    query = urllib.parse.urlencode({"jql": jql, "fields": "summary,status,assignee,priority,updated"})
    url = f"{base_url}/rest/api/2/search?{query}"
    auth = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    issues = []
    for item in payload.get("issues", []):
        fields = item.get("fields", {})
        status_name = fields.get("status", {}).get("name", "")
        assignee = fields.get("assignee", {})
        priority = fields.get("priority", {}).get("name", "")
        issues.append({
            "key": item.get("key", "N/A"),
            "summary": fields.get("summary", "No summary"),
            "status": status_name,
            "assignee": assignee.get("displayName", "Unassigned") if assignee else "Unassigned",
            "priority": priority,
            "blocked_by": "Waiting on dependency" if status_name.lower() in {"blocked", "waiting"} else "",
        })
    return issues


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


def generate_report(input_path, output_path, jira_url=None, jira_email=None, jira_token=None, project_key=None):
    issues = []
    if jira_url and jira_email and jira_token:
        try:
            issues = fetch_jira_issues(jira_url, jira_email, jira_token, project_key=project_key)
        except Exception as exc:
            print(f"Jira fetch failed: {exc}. Falling back to local data file.")
            issues = load_issues(input_path)
    else:
        issues = load_issues(input_path)

    if not issues:
        issues = load_issues(input_path)

    report = render_report(issues)
    Path(output_path).write_text(report, encoding="utf-8")
    return report


def send_report_via_email(output_path, recipient, sender, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = EmailMessage()
    msg["Subject"] = "Weekly Engineering Status Report"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(Path(output_path).read_text(encoding="utf-8"))
    msg.add_attachment(
        Path(output_path).read_bytes(),
        maintype="text",
        subtype="markdown",
        filename=Path(output_path).name,
    )

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)


def main():
    parser = argparse.ArgumentParser(description="Generate and optionally email a weekly engineering status report.")
    parser.add_argument("--input", default="jira_data.json", help="Path to a local Jira-like JSON file")
    parser.add_argument("--output", default="weekly_status_report.md", help="Path to save the markdown report")
    parser.add_argument("--send-email", action="store_true", help="Send the generated markdown file by email")
    parser.add_argument("--dry-run", action="store_true", help="Generate the markdown report without sending email")
    parser.add_argument("--jira-url", default=os.getenv("JIRA_URL"), help="Jira base URL such as https://company.atlassian.net")
    parser.add_argument("--jira-email", default=os.getenv("JIRA_EMAIL"), help="Jira account email")
    parser.add_argument("--jira-api-token", default=os.getenv("JIRA_API_TOKEN"), help="Jira API token")
    parser.add_argument("--jira-project-key", default=os.getenv("JIRA_PROJECT_KEY"), help="Optional Jira project key")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.dry_run or not args.send_email:
        report = generate_report(input_path, output_path, args.jira_url, args.jira_email, args.jira_api_token, args.jira_project_key)
        print(f"Report generated at {output_path}")
        return

    required = [
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "EMAIL_FROM",
        "EMAIL_TO",
    ]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise SystemExit(f"Missing environment variables: {', '.join(missing)}")

    report = generate_report(input_path, output_path, args.jira_url, args.jira_email, args.jira_api_token, args.jira_project_key)
    send_report_via_email(
        str(output_path),
        os.getenv("EMAIL_TO"),
        os.getenv("EMAIL_FROM"),
        os.getenv("SMTP_SERVER"),
        int(os.getenv("SMTP_PORT", "587")),
        os.getenv("SMTP_USERNAME"),
        os.getenv("SMTP_PASSWORD"),
    )
    print(f"Report generated and emailed to {os.getenv('EMAIL_TO')}")


if __name__ == "__main__":
    main()
