"""Step definitions for features/housing_eligibility.feature.

Every function here is linked to one Gherkin line by the text in its
decorator. behave reads the feature file, finds the function that matches
each line and runs it. The context object works like a shared bucket for
all the steps of one scenario: the Given steps put the values in it and the
Then steps take them out again to check them.
"""

from behave import given, when, then

from eligibility import check_eligibility


# ---- Given: what the resident typed in ----
# I keep the values as text on purpose, because that's how they arrive from a
# real form. This way the invalid examples ("thirty", "-500") go through
# exactly the same steps as the normal ones.

@given("a resident is {age} years old")
def step_resident_age(context, age):
    context.age = age


@given("they have lived in the borough for {years} years")
def step_years_in_borough(context, years):
    context.years = years


@given("their household income is {income} pounds a year")
def step_household_income(context, income):
    context.income = income


# ---- When: the resident asks for the check ----

@when("they check their eligibility")
def step_check_eligibility(context):
    # Start from nothing, so a result from another scenario can't leak in
    context.decision = None
    context.error = None
    try:
        context.decision = check_eligibility(context.age, context.years, context.income)
    except ValueError as error:
        # Keep the message instead of crashing, so a Then step can check it
        context.error = str(error)


# ---- Then: what the resident should see ----
# The text after each assert is what behave prints when the step fails,
# so I tried to make it say clearly what went wrong.

@then("they should be told they can apply to join the housing register")
def step_can_apply(context):
    assert context.error is None, f"Unexpected error: {context.error}"
    assert context.decision.eligible, f"Expected eligible, reasons were: {context.decision.reasons}"


@then("they should be told they cannot join the housing register yet")
def step_cannot_apply(context):
    assert context.error is None, f"Unexpected error: {context.error}"
    assert not context.decision.eligible, "Expected not eligible, but the resident was eligible"


@then('the reason should mention "{text}"')
def step_reason_mentions(context, text):
    # The reason only has to contain the text, so the full sentence can be
    # reworded later without breaking the scenario
    reasons = context.decision.reasons
    assert any(text in reason for reason in reasons), f"No reason mentions '{text}'. Reasons were: {reasons}"


@then('they should see the error "{message}"')
def step_see_error(context, message):
    # Here the message must match exactly, because this is what the resident reads
    assert context.error == message, f"Expected error '{message}', got '{context.error}'"


@then("no eligibility decision should be made")
def step_no_decision(context):
    assert context.decision is None, f"Expected no decision, got {context.decision}"
