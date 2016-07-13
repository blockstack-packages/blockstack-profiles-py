import json
import ecdsa
import datetime
import traceback
from keylib import ECPrivateKey, ECPublicKey
from keylib.hashing import bin_hash160
from keylib.address_formatting import bin_hash160_to_address
from keylib.key_formatting import compress, decompress
from jsontokens import TokenSigner, TokenVerifier, decode_token


class PubkeyType():
    ecdsa = 1
    uncompressed = 2
    compressed = 3


def verify_token(token, public_key_or_address, signing_algorithm="ES256K"):
    """ A function for validating an individual token.
    """
    decoded_token = decode_token(token)
    decoded_token_payload = decoded_token["payload"]

    if "subject" not in decoded_token_payload:
        raise ValueError("Token doesn't have a subject")
    if "publicKey" not in decoded_token_payload["subject"]:
        raise ValueError("Token doesn't have a subject public key")
    if "issuer" not in decoded_token_payload:
        raise ValueError("Token doesn't have an issuer")
    if "publicKey" not in decoded_token_payload["issuer"]:
        raise ValueError("Token doesn't have an issuer public key")
    if "claim" not in decoded_token_payload:
        raise ValueError("Token doesn't have a claim")

    issuer_public_key = str(decoded_token_payload["issuer"]["publicKey"])
    public_key_object = ECPublicKey(issuer_public_key)

    if public_key_object._type == PubkeyType.compressed:
        compressed_address = public_key_object.address()
        uncompressed_address = bin_hash160_to_address(
            bin_hash160(
                decompress(public_key_object.to_bin())
            )
        )
    elif public_key_object._type == PubkeyType.uncompressed:
        compressed_address = bin_hash160_to_address(
            bin_hash160(
                compress(public_key_object.to_bin())
            )
        )
        uncompressed_address = public_key_object.address()
    else:
        raise ValueError("Invalid issuer public key format")
    
    if public_key_or_address == issuer_public_key:
        pass
    elif public_key_or_address == compressed_address:
        pass
    elif public_key_or_address == uncompressed_address:
        pass
    else:
        raise ValueError("Token public key doesn't match the verifying value")

    token_verifier = TokenVerifier()

    if not token_verifier.verify(token, public_key_object.to_pem()):
        raise ValueError("Token was not signed by the issuer public key")

    return decoded_token


def verify_token_record(token_record, public_key_or_address,
                        signing_algorithm="ES256K"):
    """ A function for validating an individual token record and extracting
        the decoded token.
    """
    if "token" not in token_record:
        raise ValueError("Token record must have a token inside it")
    if "parentPublicKey" not in token_record:
        raise ValueError("Token record must have a parent public key inside it")

    token = token_record["token"]

    decoded_token = verify_token(
        token, public_key_or_address, signing_algorithm=signing_algorithm)
    token_payload = decoded_token["payload"]
    issuer_public_key = token_payload["issuer"]["publicKey"]

    if issuer_public_key == token_record["parentPublicKey"]:
        pass
    else:
        raise ValueError(
            "Verification of tokens signed with keychains is not yet supported")

    return decoded_token


def get_profile_from_tokens(token_records, public_key_or_address,
                            hierarchical_keys=False):
    """ A function for extracting a profile from a list of tokens.
    """
    
    if hierarchical_keys:
        raise NotImplementedError("Hierarchical key support not implemented")

    profile = {}

    for token_record in token_records:
        #print token_record
        try:
            decoded_token = verify_token_record(token_record, public_key_or_address)
        except ValueError:
            traceback.print_exc()
            continue
        else:
            if "payload" in decoded_token:
                if "claim" in decoded_token["payload"]:
                    claim = decoded_token["payload"]["claim"]
                    profile.update(claim)

    return profile
