"""Command-line front end so a resident can try the eligibility check."""

from eligibility import InputError, check_eligibility


def main():
    print("Housing register eligibility check")
    age = input("How old are you? ")
    years = input("How many years have you lived in the borough? ")
    income = input("What is your household income in pounds a year? ")

    try:
        decision = check_eligibility(age, years, income)
    except InputError as error:
        print(f"Sorry, we could not check that. {error}")
        return

    if decision.eligible:
        print("You can apply to join the housing register.")
    else:
        print("You cannot join the housing register yet:")
        for reason in decision.reasons:
            print(f"- {reason}")


if __name__ == "__main__":
    main()
