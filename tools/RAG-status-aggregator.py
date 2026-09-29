"""Aggregate project statuses into a red-yellow-green traffic light."""

import argparse


STATUS_LEVELS = {
    "red": 3,
    "blocked": 3,
    "critical": 3,
    "at risk": 3,
    "yellow": 2,
    "amber": 2,
    "warning": 2,
    "needs attention": 2,
    "green": 1,
    "on track": 1,
    "complete": 1,
    "completed": 1,
}
LEVEL_NAMES = {1: "GREEN", 2: "YELLOW", 3: "RED"}


def normalize_status(status: str) -> str:
    """Normalize whitespace and case for status matching."""
    return " ".join(status.strip().lower().split())


def aggregate_status(statuses: list[str]) -> str:
    """Return the highest-severity traffic-light status."""
    if not statuses:
        raise ValueError("at least one status is required")

    normalized_statuses = [normalize_status(status) for status in statuses]
    unknown_statuses = [status for status in normalized_statuses if status not in STATUS_LEVELS]
    if unknown_statuses:
        valid_statuses = ", ".join(sorted(STATUS_LEVELS))
        unknown = ", ".join(unknown_statuses)
        raise ValueError(f"unknown status: {unknown}. Valid statuses: {valid_statuses}")

    highest_level = max(STATUS_LEVELS[status] for status in normalized_statuses)
    return LEVEL_NAMES[highest_level]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate project statuses into a red-yellow-green traffic light."
    )
    parser.add_argument(
        "statuses",
        nargs="+",
        help="One or more statuses, such as green, yellow, red, blocked, or on track",
    )
    args = parser.parse_args()

    try:
        overall_status = aggregate_status(args.statuses)
    except ValueError as error:
        parser.error(str(error))

    print(f"Overall status: {overall_status}")
    print(f"Traffic light: {overall_status}")


if __name__ == "__main__":
    main()
