import json
import traceback
import unittest
from test import test_support
from keychain import PrivateKeychain, PublicKeychain
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from blockstack_profiles import sign_profile_tokens, validate_token_record, \
    get_profile_from_tokens


class TokeningTest(unittest.TestCase):
    def setUp(self):
        self.master_private_key = BitcoinPrivateKey()

    def tearDown(self):
        pass

    def test_basic_tokening(self):
        profile_components = [
            {"name": "Naval Ravikant"},
            {"birthDate": "1980-01-01"}
        ]
        reference_profile = {
            "name": "Naval Ravikant", 
            "birthDate": "1980-01-01"
        }
        # tokenize the profile
        profile_token_records = sign_profile_tokens(
            profile_components, self.master_private_key.to_hex())
        print json.dumps(profile_token_records, indent=2)
        self.assertTrue(isinstance(profile_token_records, list))
        # recover the profile
        profile = get_profile_from_tokens(
            profile_token_records, self.master_private_key.public_key().to_hex())
        print json.dumps(profile, indent=2)
        self.assertTrue(isinstance(profile, object))
        self.assertEqual(profile, reference_profile)


def test_main():
    test_support.run_unittest(
        TokeningTest,
    )


if __name__ == '__main__':
    test_main()
