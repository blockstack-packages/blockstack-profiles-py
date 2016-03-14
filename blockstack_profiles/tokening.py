import json
import ecdsa
import datetime
from keychain import PrivateKeychain, PublicKeychain
from keylib import ECPrivateKey, ECPublicKey
from jsontokens import TokenSigner, TokenVerifier, decode_token


def sign_record(claim, subject, private_key_pem, signing_algorithm="ES256K"):
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


def sign_records(profile_components, parent_private_key,
                 signing_algorithm = "ES256K"):
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
        token_record = sign_record(
            profile_component, subject, private_key.to_pem(),
            signing_algorithm=signing_algorithm)
        token_record["publicKey"] = public_key.to_hex()
        token_record["parentPublicKey"] = public_key.to_hex()
        token_records.append(token_record)

    return token_records


def validate_token_record(token_record, parent_public_key,
                          signing_algorithm = "ES256"):
    """ A function for validating an individual token record and extracting
        the decoded token.
    """

    if not ("token" in token_record and "publicKey" in token_record and \
            "parentPublicKey" in token_record):
        raise ValueError("Invalid token record")

    token = token_record["token"]

    public_key = ECPublicKey(parent_public_key)

    token_verifier = TokenVerifier()
    token_is_valid = token_verifier.verify(token, public_key.to_pem())
    if not token_is_valid:
        raise ValueError("Token is not valid")

    decoded_token = decode_token(token)
    decoded_token_payload = decoded_token["payload"]

    if "subject" not in decoded_token_payload:
        raise ValueError("Invalid decoded token")
    if "publicKey" not in decoded_token_payload["subject"]:
        raise ValueError("Invalid decoded token")
    if "claim" not in decoded_token_payload:
        raise ValueError("Invalid decoded token")

    if token_record["publicKey"] == token_record["parentPublicKey"]:
        if token_record["publicKey"] != decoded_token_payload["subject"]["publicKey"]:
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
        claim = decoded_token["payload"]["claim"]
        profile.update(claim)

    return profile
