"""Housing register eligibility check for the prototype.

The rules are simplified for the prototype. They are not the council's
real allocation policy.
"""

from dataclasses import dataclass, field

MIN_AGE = 18
MIN_YEARS_IN_BOROUGH = 2
INCOME_LIMIT = 60000  # household income must be less than this


class InputError(ValueError):
    """A value the resident typed cannot be used for the check."""


@dataclass
class Decision:
    eligible: bool
    reasons: list = field(default_factory=list)


def _whole_number(text, error_message):
    """Turn typed text into a whole number, or stop with a clear message."""
    text = str(text).strip()
    if not (text.isascii() and text.isdigit()):
        raise InputError(error_message)
    return int(text)


def check_eligibility(age, years_in_borough, income):
    age = _whole_number(age, "Age must be a whole number, for example 34.")
    years_in_borough = _whole_number(
        years_in_borough, "Years in the borough must be a whole number, for example 3.")
    income = _whole_number(
        income, "Income must be a whole number of pounds, for example 24000.")
    if years_in_borough > age:
        raise InputError("Years in the borough cannot be more than your age.")

    reasons = []
    if age < MIN_AGE:
        reasons.append(f"You must be at least {MIN_AGE} years old.")
    if years_in_borough < MIN_YEARS_IN_BOROUGH:
        reasons.append(f"You must have lived in the borough for at least {MIN_YEARS_IN_BOROUGH} years.")
    if income >= INCOME_LIMIT:
        reasons.append(f"Your household income must be less than {INCOME_LIMIT} pounds a year.")

    return Decision(eligible=not reasons, reasons=reasons)
