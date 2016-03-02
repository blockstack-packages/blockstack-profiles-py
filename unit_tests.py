import json
import traceback
import unittest
from test import test_support
from keychain import PrivateKeychain, PublicKeychain
from blockstack_profiles import sign_profile_tokens, validate_token_record, \
    get_profile_from_tokens


class TokeningTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_tokening(self):
        profile_components = [
            {"name": "Ryan Shea"}
        ]
        private_keychain = PrivateKeychain()
        profile_tokens = sign_profile_tokens(profile_components, private_keychain)
        print json.dumps(profile_tokens, indent=2)
        self.assertTrue(isinstance(profile_tokens, list))


def test_main():
    test_support.run_unittest(
        TokeningTest,
    )


if __name__ == '__main__':
    test_main()
