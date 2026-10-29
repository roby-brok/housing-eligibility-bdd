"""Housing register eligibility check.

This is the main part of the prototype. It takes what the resident typed in
(age, years in the borough and household income) and decides if they can
join the housing register, with a reason for every rule they don't meet.

The rules are simplified for the prototype. They are NOT the council's real
allocation policy, the service manager would have to give us the real ones.
"""

from dataclasses import dataclass, field

# The three rules are kept here in one place. If the council changes a limit
# we only change one number, and the scenarios will tell us straight away if
# something else breaks.
MIN_AGE = 18
MIN_YEARS_IN_BOROUGH = 2
INCOME_LIMIT = 60000  # income must be LESS than this, so 60000 itself is too much


class InputError(ValueError):
    """Something the resident typed can't be used for the check.

    It's a kind of ValueError, so code that catches ValueError catches this too.
    """


@dataclass
class Decision:
    """The answer we give back to the resident.

    eligible: True if they can apply to join the housing register.
    reasons:  one plain sentence for each rule they don't meet
              (the list is empty when they are eligible).
    """
    eligible: bool
    reasons: list = field(default_factory=list)


def _whole_number(text, error_message):
    """Turn what the resident typed into a whole number.

    On a form everything arrives as text. I only accept plain digits, so "34"
    is fine but "thirty", "-500" or "2.5" are not. In those cases the resident
    gets the friendly message we pass in, not a Python error.
    """
    text = str(text).strip()
    # isascii() is there because isdigit() also says yes to things like "²"
    if not (text.isascii() and text.isdigit()):
        raise InputError(error_message)
    return int(text)


def check_eligibility(age, years_in_borough, income):
    """Check the three rules and return a Decision.

    If any value can't be used it raises InputError, and in that case no
    decision is made at all.
    """
    # Step 1: check the input first, before looking at any rule
    age = _whole_number(age, "Age must be a whole number, for example 34.")
    years_in_borough = _whole_number(
        years_in_borough, "Years in the borough must be a whole number, for example 3.")
    income = _whole_number(
        income, "Income must be a whole number of pounds, for example 24000.")

    # Nobody can live somewhere for longer than they have been alive.
    # This rule came out when I asked "what if?" while writing the scenarios.
    if years_in_borough > age:
        raise InputError("Years in the borough cannot be more than your age.")

    # Step 2: check every rule and keep ALL the reasons, not only the first one,
    # so the resident sees everything that stops them in one go
    reasons = []
    if age < MIN_AGE:
        reasons.append(f"You must be at least {MIN_AGE} years old.")
    if years_in_borough < MIN_YEARS_IN_BOROUGH:
        reasons.append(f"You must have lived in the borough for at least {MIN_YEARS_IN_BOROUGH} years.")
    if income >= INCOME_LIMIT:
        reasons.append(f"Your household income must be less than {INCOME_LIMIT} pounds a year.")

    # No reasons means no rule was broken, so they can apply
    return Decision(eligible=not reasons, reasons=reasons)
