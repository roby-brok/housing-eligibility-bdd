# Housing Register Eligibility Check (BDD prototype)

A small Python prototype for a local authority. A resident can check if they
can join the housing register before they fill in the full application.

The expected behaviour is written as Gherkin scenarios in `features/` and
is run with [behave](https://behave.readthedocs.io/).

## Main user

A resident who needs social housing. Today they fill in a long form and can
wait weeks to find out they were never eligible. This check gives them an
answer and a clear reason straight away.

## Prototype rules

These rules are simplified for the prototype. They are not the council's real
allocation policy.

| Rule | Limit |
|---|---|
| Age | 18 or over |
| Local connection | lived in the borough for at least 2 years |
| Household income | less than 60000 pounds a year |

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m behave
```

To try the check yourself:

```bash
python main.py
```
