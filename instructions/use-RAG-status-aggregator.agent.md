# Use RAG Status Aggregator

Use `tools/RAG-status-aggregator.py` when multiple project, workstream, or delivery statuses must be reduced to one red-yellow-green traffic-light status.

## When to Use

- Use the tool when the user provides two or more status values and wants one overall project status.
- Use it for regular project, sprint, workstream, or portfolio status aggregation.
- Do not use it for weighted risk models, numeric scoring, historical trends, or statuses with custom severity rules that have not been clarified.
- Ask for the status values if the user has not provided them.

## Supported Statuses

The tool accepts these status values and aliases:

- Red-level: `red`, `blocked`, `critical`, `at risk`
- Yellow-level: `yellow`, `amber`, `warning`, `needs attention`
- Green-level: `green`, `on track`, `complete`, `completed`

Status matching is case-insensitive and repeated whitespace is normalized. Quote multi-word values such as `"at risk"` or `"on track"` when invoking the command.

## Invocation

Run the command from the project root:

```powershell
python tools/RAG-status-aggregator.py <status> [<status> ...]
```

Examples:

```powershell
python tools/RAG-status-aggregator.py green "on track" complete
python tools/RAG-status-aggregator.py green amber "needs attention"
python tools/RAG-status-aggregator.py green "on track" blocked
```

The command requires at least one status. Unknown or empty values produce a validation error; do not silently reinterpret them.

## Aggregation Rule

The tool returns the highest-severity status:

1. Any red-level status returns `RED`.
2. If there is no red-level status but at least one yellow-level status exists, return `YELLOW`.
3. If all statuses are green-level, return `GREEN`.

## Presenting Results

- Report the exact overall status returned by the tool.
- Explain the precedence that determined the result when multiple levels were supplied.
- Preserve the traffic-light wording: `GREEN`, `YELLOW`, or `RED`.
- If the result is `YELLOW` or `RED`, identify the contributing status or blocker when the input provides that context.
- If the command fails, explain that a status was missing or unsupported and request a valid value.

Example presentation:

```text
Overall status: RED
Traffic light: RED

The project is RED because one workstream is blocked. Red-level status takes precedence over yellow and green statuses.
```
