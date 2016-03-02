import jwt
import json
import ecdsa
import datetime
from keychain import PrivateKeychain, PublicKeychain
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey


def sign_profile_tokens(profile_components, parent_private_key,
                        signing_algorithm = 'ES256K'):
    """ Function for iterating through a list of profile components and
        signing separate individual profile tokens.
    """

    if signing_algorithm == 'ES256K':
        signing_algorithm = 'ES256'
    else:
        raise ValueError("Unsupported signing algorithm")

    token_records = []
    current_time = datetime.datetime.now()

    for profile_component in profile_components:
        private_key = BitcoinPrivateKey(parent_private_key)
        public_key = private_key.public_key()

        payload = {
            "claim": profile_component,
            "subject": {
                "publicKey": public_key.to_hex()
            },
            "issuedAt": current_time.isoformat(),
            "expiresAt": current_time.replace(current_time.year + 1).isoformat()
        }

        token = jwt.encode(
            payload, private_key.to_pem(), algorithm=signing_algorithm)
        decoded_token = jwt.decode(
            token, public_key.to_pem(), algorithms=[signing_algorithm])

        token_record = {
            "token": token,
            "decoded_token": decoded_token,
            "publicKey": public_key.to_hex(),
            "parentPublicKey": public_key.to_hex(),
            "encrypted": False
        }
        token_records.append(token_record)

    return token_records


def validate_token_record(token_record, parent_public_key,
                          signing_algorithm = 'ES256'):
    """ A function for validating an individual token record and extracting
        the decoded token.
    """

    if not ("token" in token_record and "publicKey" in token_record and \
            "parentPublicKey" in token_record):
        raise ValueError("Invalid token record")

    token = token_record["token"]

    public_key = BitcoinPublicKey(parent_public_key)

    decoded_token = jwt.decode(
        token, public_key.to_pem(), algorithms=[signing_algorithm])

    decoded_token = json.loads(json.dumps(decoded_token))

    if "subject" not in decoded_token and "publicKey" not in decoded_token["subject"]:
        raise ValueError("Invalid decoded token")
    if "claim" not in decoded_token:
        raise ValueError("Invalid decoded token")

    if token_record["publicKey"] == token_record["parentPublicKey"]:
        if token_record["publicKey"] != decoded_token["subject"]["publicKey"]:
            raise ValueError("Token's public key doesn't match")
    else:
        raise ValueError("Verification of tokens signed with keychains is not yet supported")

    return decoded_token


def get_profile_from_tokens(token_records, parent_public_key):
    """ A function for extracting a profile from a list of tokens.
    """

    profile = {}

    for token_record in token_records:
        decoded_token = validate_token_record(token_record, parent_public_key)
        claim = decoded_token["claim"]
        profile.update(claim)

    return profile
