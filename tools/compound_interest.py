"""Calculate compound interest from command-line inputs."""

import argparse


def calculate_compound_interest(
    principal: float,
    annual_rate_percent: float,
    compounds_per_year: int,
    total_years: float,
) -> tuple[float, float]:
    """Return the final amount and interest earned."""
    periodic_rate = annual_rate_percent / 100 / compounds_per_year
    periods = compounds_per_year * total_years
    final_amount = principal * (1 + periodic_rate) ** periods
    return final_amount, final_amount - principal


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest. Annual rate is entered as a percentage."
    )
    parser.add_argument("principal", type=positive_float, help="Initial principal amount")
    parser.add_argument(
        "annual_rate",
        type=positive_float,
        help="Annual interest rate as a percentage, such as 7.34",
    )
    parser.add_argument(
        "compounds_per_year",
        type=positive_int,
        help="Number of compounding periods per year",
    )
    parser.add_argument("total_years", type=positive_float, help="Investment duration in years")
    args = parser.parse_args()

    final_amount, interest_earned = calculate_compound_interest(
        args.principal,
        args.annual_rate,
        args.compounds_per_year,
        args.total_years,
    )

    print(f"Final amount: ${final_amount:,.2f}")
    print(f"Interest earned: ${interest_earned:,.2f}")


if __name__ == "__main__":
    main()
