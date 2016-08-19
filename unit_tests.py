import json
import traceback
import unittest
from test import test_support
from keylib import ECPrivateKey, ECPublicKey
from blockstack_profiles import (
    sign_token, wrap_token, sign_token_records,
    verify_token, verify_token_record, get_profile_from_tokens,
    make_zone_file_for_hosted_data,
    get_person_from_legacy_format,
    convert_profile_to_legacy_format,
    get_token_file_url_from_zone_file,
    zone_file_has_a_valid_uri_record,
    resolve_zone_file_to_profile
)
from test_data import reference_profiles


class VerificationTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_token_file_verification_2(self):
        token_records = reference_profiles["ryan_apr20_token_file"]
        owner_address = "1BTku19roxQs2d54kbYKVTv21oBCuHEApF"
        compressed_address = "12wes6TQpDF2j8zqvAbXV9KNCGQVF2y7G5"
        profile = get_profile_from_tokens(token_records, owner_address)
        self.assertEqual(profile["name"], "Ryan Shea")
        profile = get_profile_from_tokens(token_records, compressed_address)
        self.assertEqual(profile["name"], "Ryan Shea")


class TokeningTests(unittest.TestCase):
    def setUp(self):
        self.master_private_key = ECPrivateKey(compressed=True)
        self.profile_components = [
            {"name": "Naval Ravikant"},
            {"birthDate": "1980-01-01"}
        ]

    def tearDown(self):
        pass

    def test_token_verification_and_recovery(self):
        # tokenize the profile
        profile_token_records = sign_token_records(
            self.profile_components, self.master_private_key.to_hex())
        #print json.dumps(profile_token_records, indent=2)
        self.assertTrue(isinstance(profile_token_records, list))
        # verify the token records
        for token_record in profile_token_records:
            public_key = self.master_private_key.public_key().to_hex()
            decoded_token = verify_token_record(token_record, public_key)
            self.assertTrue(isinstance(decoded_token, dict))

        # recover the profile
        profile = get_profile_from_tokens(
            profile_token_records, self.master_private_key.public_key().to_hex())
        # print json.dumps(profile, indent=2)
        self.assertTrue(isinstance(profile, object))
        self.assertEqual(profile, reference_profiles["naval"])

    def test_token_verification_with_address(self):
        profile_token_records = sign_token_records(
            self.profile_components, self.master_private_key.to_hex())
        self.assertTrue(isinstance(profile_token_records, list))

        for token_record in profile_token_records:
            address = self.master_private_key.public_key().address()
            decoded_token = verify_token_record(token_record, address)
            self.assertTrue(isinstance(decoded_token, dict))

    def test_token_verification_with_public_key(self):
        public_key = "0273be63a7091923467111e09bbd54492a65b709c7a02416860bd55d7c496bf009"
        token_records = []

        with open('test_data/sample_token.json', 'r') as f:
            data = f.read()
            token_records = json.loads(data)

        for token_record in token_records:
            token_verified = verify_token_record(token_record, public_key)
            self.assertTrue(token_verified)

    def test_token_file_verification(self):
        token_records = reference_profiles["naval_token_file"]
        public_key = "038354d097be9004f63a6409e2c7a05467b1950120b4c5f840f99832dad743ac1e"
        profile = get_profile_from_tokens(token_records, public_key)


class ZonefileTests(unittest.TestCase):
    def setUp(self):
        self.zone_file = """$ORIGIN naval.id
$TTL 3600
_http._tcp URI 10 1 \"https://mq9.s3.amazonaws.com/naval.id/profile.json\""""
        self.zone_file_2 = """$ORIGIN ryan_apr20.id
$TTL 3600
_http._tcp URI 10 1 \"https://blockstack.s3.amazonaws.com/ryan_apr20.id\""""
        self.public_key_2 = "02413d7c51118104cfe1b41e540b6c2acaaf91f1e2e22316df7448fb6070d582ec"

    def tearDown(self):
        pass

    def test_zone_file_creation(self):
        origin = "naval.id"
        token_file_url = "https://mq9.s3.amazonaws.com/naval.id/profile.json"
        zone_file = make_zone_file_for_hosted_data(origin, token_file_url)
        # print zone_file
        self.assertTrue(isinstance(zone_file, (unicode, str)))
        self.assertTrue("$ORIGIN" in zone_file)
        self.assertTrue("$TTL" in zone_file)
        self.assertTrue("_http._tcp URI" in zone_file)

    def test_token_file_url_recovery_from_zone_file(self):
        token_file_url = get_token_file_url_from_zone_file(self.zone_file)
        self.assertEqual(token_file_url, "https://mq9.s3.amazonaws.com/naval.id/profile.json")

    def test_zone_file_has_a_valid_uri_record(self):
        is_valid = zone_file_has_a_valid_uri_record(self.zone_file)
        self.assertTrue(is_valid)

    def test_resolve_zone_file_to_profile(self):
        profile, error = resolve_zone_file_to_profile(self.zone_file_2, self.public_key_2)

        self.assertTrue("name" in profile)


class LegacyFormatTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_profile_format_migration(self):
        zone_file = get_person_from_legacy_format(reference_profiles["jude"])
        # print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))

    def test_format_conversion_to_legacy(self):
        legacy_format = convert_profile_to_legacy_format(reference_profiles["ryan_new"])
        #print json.dumps(legacy_format, indent=2, sort_keys=True)
        self.assertTrue(isinstance(legacy_format, dict))


def test_main():
    test_support.run_unittest(
        VerificationTests,
        TokeningTests,
        ZonefileTests,
        LegacyFormatTests
    )


if __name__ == '__main__':
    test_main()
