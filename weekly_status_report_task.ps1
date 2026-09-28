$ErrorActionPreference = "Stop"

# Set Jira and Outlook values before scheduling this task.
$env:JIRA_URL = "https://your-company.atlassian.net"
$env:JIRA_EMAIL = "your-jira-user@company.com"
$env:JIRA_API_TOKEN = "your-jira-api-token"
$env:JIRA_PROJECT_KEY = "PROJ"

$env:SMTP_SERVER = "smtp.office365.com"
$env:SMTP_PORT = "587"
$env:SMTP_USERNAME = "your-outlook-user@company.com"
$env:SMTP_PASSWORD = "your-app-password-or-token"
$env:EMAIL_FROM = "your-outlook-user@company.com"
$env:EMAIL_TO = "distribution-list@company.com"

python "C:\workspace\hello-genai\weekly_status_report_email.py" --input "C:\workspace\hello-genai\jira_data.json" --output "C:\workspace\hello-genai\weekly_status_report.md" --send-email
