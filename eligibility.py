"""Housing register eligibility check for the prototype.

The rules are simplified for the prototype. They are not the council's
real allocation policy.
"""

from dataclasses import dataclass, field

MIN_AGE = 18
MIN_YEARS_IN_BOROUGH = 2
INCOME_LIMIT = 60000  # household income must be less than this


@dataclass
class Decision:
    eligible: bool
    reasons: list = field(default_factory=list)


def check_eligibility(age, years_in_borough, income):
    age = int(age)
    years_in_borough = int(years_in_borough)
    income = int(income)

    reasons = []
    if age < MIN_AGE:
        reasons.append(f"You must be at least {MIN_AGE} years old.")
    if years_in_borough < MIN_YEARS_IN_BOROUGH:
        reasons.append(f"You must have lived in the borough for at least {MIN_YEARS_IN_BOROUGH} years.")
    if income >= INCOME_LIMIT:
        reasons.append(f"Your household income must be less than {INCOME_LIMIT} pounds a year.")

    return Decision(eligible=not reasons, reasons=reasons)
