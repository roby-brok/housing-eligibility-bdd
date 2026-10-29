"""Small command-line version of the eligibility check.

This isn't the real council website, it's just a quick way for a resident
(or a service manager in a demo) to try the rules.

I kept all the rules out of this file on purpose. Writing the acceptance
tests first pushed the business rules away from the user interface, so behave
can call check_eligibility() directly without anybody typing into a screen.
If this becomes a web form later, the rules and the scenarios stay the same,
only this file changes.
"""

from eligibility import InputError, check_eligibility


def main():
    print("Housing register eligibility check")
    # input() always gives back text, that's fine because eligibility.py checks it
    age = input("How old are you? ")
    years = input("How many years have you lived in the borough? ")
    income = input("What is your household income in pounds a year? ")

    try:
        decision = check_eligibility(age, years, income)
    except InputError as error:
        # Show the friendly message from eligibility.py, not a Python error
        print(f"Sorry, we could not check that. {error}")
        return

    if decision.eligible:
        print("You can apply to join the housing register.")
    else:
        # Print every reason, so the resident knows everything that is missing
        print("You cannot join the housing register yet:")
        for reason in decision.reasons:
            print(f"- {reason}")


# Only run main() when the file is started directly (python main.py),
# not when another file imports it
if __name__ == "__main__":
    main()
