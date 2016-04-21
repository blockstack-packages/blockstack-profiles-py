import json
import ecdsa
import datetime
from keylib import ECPrivateKey, ECPublicKey
from jsontokens import TokenSigner, TokenVerifier, decode_token


def sign_token(claim, signing_private_key, subject, issuer=None,
               signing_algorithm="ES256K"):
    if signing_algorithm != 'ES256K':
        raise ValueError("Signing algorithm not supported")

    private_key_object = ECPrivateKey(signing_private_key)
    public_key_hex = private_key_object.public_key().to_hex()

    if not issuer:
        issuer = {
            "publicKey": public_key_hex
        }

    current_time = datetime.datetime.now()

    payload = {
        "claim": claim,
        "subject": subject,
        "issuer": issuer,
        "issuedAt": current_time.isoformat(),
        "expiresAt": current_time.replace(current_time.year + 1).isoformat()
    }

    token_signer = TokenSigner()
    token = token_signer.sign(payload, private_key_object.to_pem())

    return token


def wrap_token(token):
    token_record = {
        "token": token,
        "decodedToken": decode_token(token),
        "encrypted": False
    }
    return token_record


def sign_token_records(profile_components, parent_private_key,
                       signing_algorithm="ES256K"):
    """ Function for iterating through a list of profile components and
        signing separate individual profile tokens.
    """

    if signing_algorithm != "ES256K":
        raise ValueError("Signing algorithm not supported")

    token_records = []

    for profile_component in profile_components:
        private_key = ECPrivateKey(parent_private_key)
        public_key = private_key.public_key()
        subject = {
            "publicKey": public_key.to_hex()
        }
        token = sign_token(profile_component, private_key.to_hex(), subject,
                           signing_algorithm=signing_algorithm)
        token_record = wrap_token(token)
        token_record["parentPublicKey"] = public_key.to_hex()
        token_records.append(token_record)

    return token_records
