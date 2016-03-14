#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    blockstack-profiles-py
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of blockstack-profiles-py

    Blockstack-profiles-py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Blockstack-profiles-py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with blockstack-profiles-py.  If not, see <http://www.gnu.org/licenses/>.
"""

def format_account(service_name, data):
    """
    Given profile data and the name of a
    social media service, format it for
    the zone file.

    @serviceName: name of the service
    @data: legacy profile verification

    Returns the formatted account on success,
    as a dict.
    """

    assert 'username' in data, "Missing username"

    account = {
        "@type": "Account",
        "service": service_name,
        "identifier": data["username"],
        "proofType": "http"
    }
    if data.has_key(service_name) and data[service_name].has_key("proof"):
        account["proofUrl"] = data[service_name]["proof"]

    return account


def get_person_from_legacy_format(profile_record):
    """
    Given a whole profile, convert it into 
    zone-file format.  In the full profile JSON,
    this method operates on the 'data_record' object.

    @profile is a dict that contains the legacy profile data

    Return a dict with the zone-file formatting.
    """

    assert is_profile_in_legacy_format(profile_record), "Not a legacy profile"

    profile = profile_record

    images = []
    accounts = []
    profile_data = {
        "@type": "Person"
    }

    if profile.has_key("name") and type(profile["name"]) == dict \
            and profile["name"].has_key("formatted"):
        profile_data["name"] = profile["name"]["formatted"]

    if profile.has_key("bio"):
        profile_data["bio"] = profile["bio"]

    if profile.has_key("location") and type(profile["location"]) == dict \
            and profile["location"].has_key("formatted"):
        profile_data["address"] = {
            "@type": "PostalAddress",
            "addressLocality": profile["location"]["formatted"]
        }

    if profile.has_key("avatar") and type(profile["avatar"]) == dict and \
            profile["avatar"].has_key("url"):
        images.append({
            "@type": "ImageObject",
            "name": "avatar",
            "contentUrl": profile["avatar"]["url"]
        })

    if profile.has_key("cover") and type(profile["cover"]) == dict and \
            profile["cover"].has_key("url"):
        images.append({
            "@type": "ImageObject",
            "name": "cover",
            "contentUrl": profile["cover"]["url"]
        })

    if len(images) > 0:
        profile_data["image"] = images

    if profile.has_key("website") and type(profile["website"]) in [str, unicode]:
        profile_data["website"] = [{
            "@type": "WebSite",
            "url": profile["website"]
        }]

    if profile.has_key("bitcoin") and type(profile["bitcoin"]) == dict and \
            profile["bitcoin"].has_key("address"):
        accounts.append({
            "@type": "Account",
            "role": "payment",
            "service": "bitcoin",
            "identifier": profile["bitcoin"]["address"]
        })

    for service_name in ["twitter', 'facebook', 'github"]:
        if profile.has_key(service_name):
            accounts.append(
                format_account(service_name, profile[service_name])
            )

    if profile.has_key("auth"):
        if len(profile["auth"]) > 0 and type(profile["auth"]) == dict:
            if profile["auth"][0].has_key("publicKeychain"):
                accounts.append({
                    "@type": "Account",
                    "role": "key",
                    "service": "bip32",
                    "identifier": profile["auth"][0]["publicKeychain"]
                })

    if profile.has_key("pgp") and type(profile["pgp"]) == dict \
            and profile["pgp"].has_key("url") \
            and profile["pgp"].has_key("fingerprint"):
        accounts.append({
            "@type": "Account",
            "role": "key",
            "service": "pgp",
            "identifier": profile["pgp"]["fingerprint"],
            "contentUrl": profile["pgp"]["url"]
        })

    profile_data["accounts"] = accounts 

    return profile_data


def is_profile_in_legacy_format(profile):
    """
    Is a given profile JSON object in legacy format?
    """
    is_in_legacy_format = False

    if profile.has_key("avatar"):
        is_in_legacy_format = True

    if profile.has_key("bio"):
        is_in_legacy_format = True

    return is_in_legacy_format
