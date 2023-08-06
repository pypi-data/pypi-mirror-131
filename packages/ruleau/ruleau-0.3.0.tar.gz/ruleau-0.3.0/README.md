# Ruleau

A Python Rules Engine library

## Using the library

```python
from ruleau import execute, rule, ApiAdapter

# create a rule
@rule(rule_id="rul_1", name="Is adult")
def over_18(_, payload):
    return "age" in payload and payload["age"] >= 18

# create a payload (the answers to the rule's questions)
payload = {"age": 17}

# execute the rule against the payload
result = execute(over_18, payload)

# integrate with the backend web API
api_adapter = ApiAdapter(base_url="http://localhost:8000/")

# send the results
result = execute(
    over_18, payload, api_adapter=api_adapter, case_id="ca_1280"
)
# result.result will be False due to applicant being 17

# if the rule for this case is overriden in the backend
# then running again will return True

```

### Testing Rules

Rules should be tested using [doctest](https://docs.python.org/3/library/doctest.html).

Example of these tests can be found in the [Kitchen Sink example](https://gitlab.com/unai-ltd/unai-decision/ruleau-core/-/tree/develop/examples/kitchen_sink/rules.py).

### Generating Documentation

Documentation for the rules can be generated using the `ruleau-docs` command.

The usage is as follows:
```
ruleau-docs [--output-dir=<argument>] filename
```

For example for a file of rules called `rules.py` run: 
```
ruleau-docs rules.py
```
