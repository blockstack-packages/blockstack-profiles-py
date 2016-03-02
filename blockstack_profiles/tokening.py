import jwt
import ecdsa
from keychain import PrivateKeychain, PublicKeychain

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def sign_profile_tokens(profile_components, private_keychain,
                        signing_algorithm = 'ES256K'):
    if not isinstance(private_keychain, PrivateKeychain):
        raise ValueError("private_keychain must be a valid PrivateKeychain object")

    if signing_algorithm == 'ES256K':
        signing_algorithm = 'ES256'
    else:
        raise ValueError("Unsupported signing algorithm")

    token_records = []

    for profile_component in profile_components:
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        payload = {
            "claim": {},
            "subject": {
                "publicKey": ""
            },
            "issuedAt": "",
            "expiresAt": ""
        }

        token = jwt.encode(payload, pem_private_key, algorithm=signing_algorithm)
        decoded_token = jwt.decode(token, pem_public_key, algorithms=[signing_algorithm])

        token_record = {
            "token": token,
            "data": decoded_token,
            "publicKey": "",
            "parentPublicKey": "",
            "derivationEntropy": "",
            "encrypted": False
        }
        token_records.append(token_record)

    return token_records

def validate_token_record(token_record, public_keychain):
    return None

def get_profile_from_tokens(token_records, public_keychain):
    return None

