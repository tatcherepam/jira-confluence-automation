# Calculate Compound Interest

Use `tools/compound_interest.py` when the user needs compound-interest calculations from a principal, annual percentage rate, compounding frequency, and duration.

## When to Use

- Use this instruction for compound-interest calculations with regular compounding periods.
- Use the existing Python tool instead of calculating manually when the user provides all four required inputs.
- Ask for any missing input before invoking the tool:
  - Principal amount.
  - Annual interest rate as a percentage, such as `7.34`.
  - Compounding periods per year, such as `12` for monthly.
  - Total duration in years. Fractional years are allowed, such as `8.5833333333` for 8 years and 7 months.
- Do not use this tool for simple interest, continuously compounded interest, irregular deposits, or changing rates without first clarifying the calculation model.

## Invocation

Run the command from the project root:

```powershell
python tools/compound_interest.py <principal> <annual_rate_percent> <compounds_per_year> <total_years>
```

Example for $15,847 at 7.34%, compounded monthly, for 8 years and 7 months:

```powershell
python tools/compound_interest.py 15847 7.34 12 8.583333333333333
```

Arguments are positional and must be supplied in this order:

1. `principal`: positive initial amount.
2. `annual_rate_percent`: positive annual rate expressed as a percentage, not a decimal. Use `7.34`, not `0.0734`.
3. `compounds_per_year`: positive whole number, such as `1`, `4`, `12`, or `365`.
4. `total_years`: positive duration in years; fractional values are supported.

The tool rejects zero or negative values. Correct the inputs rather than bypassing validation.

## Result Presentation

- Report both values returned by the tool:
  - `Final amount`
  - `Interest earned`
- Preserve currency formatting to two decimal places.
- State the input assumptions, including the compounding frequency and duration.
- If the duration was converted from years and months, mention the conversion and total number of compounding periods.
- Do not present interest earned as the final amount; interest is the final amount minus the principal.
- If the command fails, explain which input is missing or invalid and request a corrected value.

Example response format:

```text
Using monthly compounding for 8 years and 7 months (103 monthly periods):

Final amount: $29,697.95
Interest earned: $13,850.95
```
