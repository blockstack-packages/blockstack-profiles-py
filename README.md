# Blockstack Profiles Python

[![CircleCI](https://img.shields.io/circleci/project/blockstack/blockstack-profiles-py/master.svg)](https://circleci.com/gh/blockstack/blockstack-profiles-py)
[![PyPI](https://img.shields.io/pypi/v/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![PyPI](https://img.shields.io/pypi/dm/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![PyPI](https://img.shields.io/pypi/l/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![Slack](http://slack.blockstack.org/badge.svg)](http://slack.blockstack.org/)

### Installation

```bash
$ pip install blockstack-profiles
```

If you have any trouble with the installation, see [the troubleshooting guide](/troubleshooting.md) for guidance on common issues.

### Importing

```python
from blockstack_profiles import (
  sign_token, wrap_token, sign_token_records,
  validate_token_record, get_profile_from_tokens
)
```

### Creating Profiles

```python
profile = { "name": "Naval Ravikant", "birthDate": "1980-01-01" }
profile_components = [
    {"name": "Naval Ravikant"},
    {"birthDate": "1980-01-01"}
]
```

### Tokenizing Profiles

```python
token_records = sign_token_records(profile_components, "89088e4779c49c8c3210caae38df06193359417036d87d3cc8888dcfe579905701")
```

### Verifying Token Records

#### Verifying Against Public Keys

```python
public_key = "030589ee559348bd6a7325994f9c8eff12bd5d73cc683142bd0dd1a17abc99b0dc"
decoded_token = verify_token_record(token_records[0], public_key)
```

#### Verifying Against Addresses

```python
address = "1KbUJ4x8epz6QqxkmZbTc4f79JbWWz6g37"
decoded_token = verify_token_record(token_records[0], address)
```

### Recovering Profiles

```python
profile = get_profile_from_tokens(profile_tokens, "02f1fd79dcd51bd017f71546ddc0fd3c8fb7de673da8661c4ceec0463dc991cc7e")
```

```
>>> print profile
{
  "name": "Naval Ravikant", 
  "birthDate": "1980-01-01"
}
```
