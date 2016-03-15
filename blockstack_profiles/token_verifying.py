import json
import ecdsa
import datetime
from keychain import PrivateKeychain, PublicKeychain
from keylib import ECPrivateKey, ECPublicKey
from jsontokens import TokenSigner, TokenVerifier, decode_token


def validate_token_record(token_record, public_key,
                          signing_algorithm="ES256"):
    """ A function for validating an individual token record and extracting
        the decoded token.
    """

    if not ("token" in token_record and "publicKey" in token_record and \
            "parentPublicKey" in token_record):
        raise ValueError("Invalid token record")

    token = token_record["token"]

    public_key = ECPublicKey(public_key)

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
        raise ValueError(
            "Verification of tokens signed with keychains is not yet supported")

    return decoded_token


def get_profile_from_tokens(token_records, public_key,
                            hierarchical_keys=False):
    """ A function for extracting a profile from a list of tokens.
    """
    
    if hierarchical_keys == True:
        raise Exception("Hierarchical key ")

    profile = {}

    for token_record in token_records:
        try:
            decoded_token = validate_token_record(token_record, public_key)
        except ValueError:
            continue
        else:
            claim = decoded_token["payload"]["claim"]
            profile.update(claim)

    return profile
