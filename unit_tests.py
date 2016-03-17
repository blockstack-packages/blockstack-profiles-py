import json
import traceback
import unittest
from test import test_support
from keychain import PrivateKeychain, PublicKeychain
from keylib import ECPrivateKey, ECPublicKey
from blockstack_profiles import (
    sign_token_record, sign_token_records, verify_token_record,
    get_profile_from_tokens,
    make_zone_file_for_hosted_data,
    get_person_from_legacy_format 
)
from test_data import reference_profiles


class TokeningTests(unittest.TestCase):
    def setUp(self):
        self.master_private_key = ECPrivateKey(compressed=True)

    def tearDown(self):
        pass

    def test_basic_tokening(self):
        profile_components = [
            {"name": "Naval Ravikant"},
            {"birthDate": "1980-01-01"}
        ]
        # tokenize the profile
        profile_token_records = sign_token_records(
            profile_components, self.master_private_key.to_hex())
        # print json.dumps(profile_token_records, indent=2)
        self.assertTrue(isinstance(profile_token_records, list))
        # verify the token records
        for token_record in profile_token_records:
            decoded_token = verify_token_record(token_record, self.master_private_key.public_key().to_hex())
            self.assertTrue(isinstance(decoded_token, dict))
        # recover the profile
        profile = get_profile_from_tokens(
            profile_token_records, self.master_private_key.public_key().to_hex())
        # print json.dumps(profile, indent=2)
        self.assertTrue(isinstance(profile, object))
        self.assertEqual(profile, reference_profiles["naval"])


class ZonefileTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zone_file_creation(self):
        origin = "naval.id"
        token_file_url = "https://mq9.s3.amazonaws.com/naval.id/profile.json"
        zone_file = make_zone_file_for_hosted_data(origin, token_file_url)
        # print zone_file
        self.assertTrue(isinstance(zone_file, (unicode, str)))


class LegacyFormatTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_profile_format_migration(self):
        zone_file = get_person_from_legacy_format(reference_profiles["jude"])
        # print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))

    def test_profile_format_migration_2(self):
        zone_file = get_person_from_legacy_format(reference_profiles["muneeb"])
        # print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))


def test_main():
    test_support.run_unittest(
        TokeningTests,
        ZonefileTests,
        LegacyFormatTests
    )


if __name__ == '__main__':
    test_main()
