import json
import ecdsa
import datetime
from keylib import ECPrivateKey, ECPublicKey
from jsontokens import TokenSigner, TokenVerifier, decode_token


def sign_token_record(claim, subject, private_key_pem,
                      signing_algorithm="ES256K"):
    current_time = datetime.datetime.now()

    payload = {
        "claim": claim,
        "subject": subject,
        "issuedAt": current_time.isoformat(),
        "expiresAt": current_time.replace(current_time.year + 1).isoformat()
    }

    token_signer = TokenSigner()
    token = token_signer.sign(payload, private_key_pem)
    decoded_token = decode_token(token)

    token_record = {
        "token": token,
        "decodedToken": decoded_token,
        "encrypted": False
    }
    return token_record


def sign_token_records(profile_components, parent_private_key,
                       signing_algorithm="ES256K"):
    """ Function for iterating through a list of profile components and
        signing separate individual profile tokens.
    """

    if signing_algorithm == "ES256K":
        signing_algorithm = "ES256"
    else:
        raise ValueError("Unsupported signing algorithm")

    token_records = []

    for profile_component in profile_components:
        private_key = ECPrivateKey(parent_private_key)
        public_key = private_key.public_key()
        subject = {
            "publicKey": public_key.to_hex()
        }
        token_record = sign_token_record(
            profile_component, subject, private_key.to_pem(),
            signing_algorithm=signing_algorithm)
        token_record["publicKey"] = public_key.to_hex()
        token_record["parentPublicKey"] = public_key.to_hex()
        token_records.append(token_record)

    return token_records