# Blockstack Profiles Python

[![Slack](http://slack.blockstack.org/badge.svg)](http://slack.blockstack.org/)

### Importing

```python
from blockstack_profiles import sign_profile_tokens, validate_token_record, get_profile_from_tokens
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
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
master_private_key = BitcoinPrivateKey()
token_records = sign_profile_tokens(profile_components, master_private_key.to_hex())
```

```python
>>> print token_records
[
  {
    "decoded_token": {
      "issuedAt": "2016-03-02T17:14:03.183718", 
      "claim": {
        "name": "Naval Ravikant"
      }, 
      "expiresAt": "2017-03-02T17:14:03.183718", 
      "subject": {
        "publicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7"
      }
    }, 
    "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjIwMTYtMDMtMDJUMTc6MTQ6MDMuMTgzNzE4IiwiY2xhaW0iOnsibmFtZSI6Ik5hdmFsIFJhdmlrYW50In0sImV4cGlyZXNBdCI6IjIwMTctMDMtMDJUMTc6MTQ6MDMuMTgzNzE4Iiwic3ViamVjdCI6eyJwdWJsaWNLZXkiOiIwNDU4YzZmNDI1ZGMwYmM2M2ZiOWZkYTkwZGYzNTJhOGNmNjJiZjE4MmZkMThjNmY3YWFjMGFlZWE0NTQ1ODRiZWM0YWZiOWE3MzRiZjBjN2M0ZTc1YWJhNTc0MTY2ZGNjZjU0NDg2NzMwYjZmMjc2MDU0MWIxMmMyY2NkMzRkMGQ3In19.7rht4NcfeWZlOQn3eoXLNH90o1Pz4WPQ3A9t3Nvgw7GZ7ez1p8doF2tFsi58o9L5v-avpcWK6Y_uUXSRCEPcZQ", 
    "parentPublicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7", 
    "encrypted": false, 
    "publicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7"
  }, 
  {
    "decoded_token": {
      "issuedAt": "2016-03-02T17:14:03.183718", 
      "claim": {
        "birthDate": "1980-01-01"
      }, 
      "expiresAt": "2017-03-02T17:14:03.183718", 
      "subject": {
        "publicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7"
      }
    }, 
    "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjIwMTYtMDMtMDJUMTc6MTQ6MDMuMTgzNzE4IiwiY2xhaW0iOnsiYmlydGhEYXRlIjoiMTk4MC0wMS0wMSJ9LCJleHBpcmVzQXQiOiIyMDE3LTAzLTAyVDE3OjE0OjAzLjE4MzcxOCIsInN1YmplY3QiOnsicHVibGljS2V5IjoiMDQ1OGM2ZjQyNWRjMGJjNjNmYjlmZGE5MGRmMzUyYThjZjYyYmYxODJmZDE4YzZmN2FhYzBhZWVhNDU0NTg0YmVjNGFmYjlhNzM0YmYwYzdjNGU3NWFiYTU3NDE2NmRjY2Y1NDQ4NjczMGI2ZjI3NjA1NDFiMTJjMmNjZDM0ZDBkNyJ9fQ.gMot7lpsZeVJcl8vBtMkEGGK97NJWrLgh3b5kPXFeu4L2NmEUkq1PXpn3I8iwRDneAXnXmlGunz1P1LgTZDqhw", 
    "parentPublicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7", 
    "encrypted": false, 
    "publicKey": "0458c6f425dc0bc63fb9fda90df352a8cf62bf182fd18c6f7aac0aeea454584bec4afb9a734bf0c7c4e75aba574166dccf54486730b6f2760541b12c2ccd34d0d7"
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