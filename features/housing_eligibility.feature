Feature: Housing register eligibility check
  As a resident who needs social housing
  I want to check if I can join the housing register before I apply
  So that I do not spend time on an application that will be refused

  Scenario Outline: Resident who meets all the rules can apply
    Given a resident is <age> years old
    And they have lived in the borough for <years> years
    And their household income is <income> pounds a year
    When they check their eligibility
    Then they should be told they can apply to join the housing register

    Examples: Typical resident and resident exactly on the limits
      | age | years | income |
      | 34  | 5     | 24000  |
      | 18  | 2     | 59999  |

  Scenario Outline: Resident just outside one rule is told the reason
    Given a resident is <age> years old
    And they have lived in the borough for <years> years
    And their household income is <income> pounds a year
    When they check their eligibility
    Then they should be told they cannot join the housing register yet
    And the reason should mention "<reason>"

    Examples: One value just past each limit
      | age | years | income | reason                                     |
      | 17  | 5     | 24000  | at least 18 years old                      |
      | 34  | 1     | 24000  | lived in the borough for at least 2 years  |
      | 34  | 5     | 60000  | less than 60000 pounds a year              |

  Scenario Outline: Resident enters a value the check cannot use
    Given a resident is <age> years old
    And they have lived in the borough for <years> years
    And their household income is <income> pounds a year
    When they check their eligibility
    Then they should see the error "<error>"
    And no eligibility decision should be made

    Examples: Invalid or impossible values
      | age    | years | income | error                                                       |
      | thirty | 5     | 24000  | Age must be a whole number, for example 34.                 |
      | 34     | 5     | -500   | Income must be a whole number of pounds, for example 24000. |
      | 34     | 40    | 24000  | Years in the borough cannot be more than your age.          |
