# Blockstack Profiles Python

[![CircleCI](https://img.shields.io/circleci/project/blockstack/blockstack-profiles-py.svg)](https://circleci.com/gh/blockstack/blockstack-profiles-py)
[![PyPI](https://img.shields.io/pypi/v/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![PyPI](https://img.shields.io/pypi/dm/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![PyPI](https://img.shields.io/pypi/l/blockstack-profiles.svg)](https://pypi.python.org/pypi/blockstack-profiles/)
[![Slack](http://slack.blockstack.org/badge.svg)](http://slack.blockstack.org/)

### Importing

```python
from blockstack_profiles import sign_token_records, get_profile_from_tokens, make_zone_file_for_hosted_file
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
token_records = sign_token_records(profile_components, 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
```

```python
>>> print token_records
[
  {
    "decoded_token": {
      "issuedAt": "2016-03-02T18:59:29.043308", 
      "claim": {
        "name": "Naval Ravikant"
      }, 
      "expiresAt": "2017-03-02T18:59:29.043308", 
      "subject": {
        "publicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268"
      }
    }, 
    "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjIwMTYtMDMtMDJUMTg6NTk6MjkuMDQzMzA4IiwiY2xhaW0iOnsibmFtZSI6Ik5hdmFsIFJhdmlrYW50In0sImV4cGlyZXNBdCI6IjIwMTctMDMtMDJUMTg6NTk6MjkuMDQzMzA4Iiwic3ViamVjdCI6eyJwdWJsaWNLZXkiOiIwM2U5OTUzY2IxODRiMGMyNTNlMWM1YTk2ZGY0Y2I5OTMzYmY4OWVkMmRmNWJkNzliMDJmNzFjY2ZlNWVjNTAyNjgifX0.0qQbEXTsDSbswL2qfMVzMuYU503ddfclXz3ict1rh85arXX47DW51814n1OFOAzjGoeDvsQXpfG3hB2dMHuIEw", 
    "parentPublicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268", 
    "encrypted": false, 
    "publicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268"
  }, 
  {
    "decoded_token": {
      "issuedAt": "2016-03-02T18:59:29.043308", 
      "claim": {
        "birthDate": "1980-01-01"
      }, 
      "expiresAt": "2017-03-02T18:59:29.043308", 
      "subject": {
        "publicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268"
      }
    }, 
    "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjIwMTYtMDMtMDJUMTg6NTk6MjkuMDQzMzA4IiwiY2xhaW0iOnsiYmlydGhEYXRlIjoiMTk4MC0wMS0wMSJ9LCJleHBpcmVzQXQiOiIyMDE3LTAzLTAyVDE4OjU5OjI5LjA0MzMwOCIsInN1YmplY3QiOnsicHVibGljS2V5IjoiMDNlOTk1M2NiMTg0YjBjMjUzZTFjNWE5NmRmNGNiOTkzM2JmODllZDJkZjViZDc5YjAyZjcxY2NmZTVlYzUwMjY4In19.m-v3mrPtXaNSltBvWfOLnpPerIxJhQQOt0-x-Lyw1A-iGp_dq8TPLrYGqo4UfcBfqva52-N5eSCN6c1pKgSLDQ", 
    "parentPublicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268", 
    "encrypted": false, 
    "publicKey": "03e9953cb184b0c253e1c5a96df4cb9933bf89ed2df5bd79b02f71ccfe5ec50268"
  }
]
```

### Recovering Profiles

```python
master_public_key = master_private_key.public_key()
profile = get_profile_from_tokens(profile_tokens, master_public_key.to_hex())
```

```
>>> print profile
{
  "name": "Naval Ravikant", 
  "birthDate": "1980-01-01"
}
```

### Creating Zone Files

```python
zone_file = make_zone_file_for_hosted_file("naval.id", "https://mq9.s3.amazonaws.com/naval.id/profile.json")
```

```python
$ORIGIN naval.id
$TTL 3600
@ IN URI https://mq9.s3.amazonaws.com/naval.id/profile.json
```
