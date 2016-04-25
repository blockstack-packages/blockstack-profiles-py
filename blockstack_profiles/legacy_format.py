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

import json


def is_profile_in_legacy_format(profile):
    """
    Is a given profile JSON object in legacy format?
    """
    if isinstance(profile, dict):
        pass
    elif isinstance(profile, (str, unicode)):
        try:
            profile = json.loads(profile)
        except ValueError:
            return False
    else:
        return False

    if profile.has_key("@type"):
        return False

    if profile.has_key("@context"):
        return False

    is_in_legacy_format = False

    if profile.has_key("avatar"):
        is_in_legacy_format = True
    elif profile.has_key("cover"):
        is_in_legacy_format = True
    elif profile.has_key("bio"):
        is_in_legacy_format = True
    elif profile.has_key("twitter"):
        is_in_legacy_format = True
    elif profile.has_key("facebook"):
        is_in_legacy_format = True

    return is_in_legacy_format


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

    if "username" not in data:
        raise KeyError("Account is missing a username")

    account = {
        "@type": "Account",
        "service": service_name,
        "identifier": data["username"],
        "proofType": "http"
    }

    if (data.has_key(service_name)
        and data[service_name].has_key("proof")
        and data[service_name]["proof"].has_key("url")):
        account["proofUrl"] = data[service_name]["proof"]["url"]

    return account


def get_person_from_legacy_format(profile_record):
    """
    Given a whole profile, convert it into 
    zone-file format.  In the full profile JSON,
    this method operates on the 'data_record' object.

    @profile is a dict that contains the legacy profile data

    Return a dict with the zone-file formatting.
    """

    if not is_profile_in_legacy_format(profile_record):
        raise ValueError("Not a legacy profile")

    profile = profile_record

    try:
        profile = json.loads(json.dumps(profile))
    except ValueError:
        pass

    images = []
    accounts = []
    profile_data = {
        "@type": "Person"
    }

    if profile.has_key("name") and type(profile["name"]) == dict \
            and profile["name"].has_key("formatted"):
        profile_data["name"] = profile["name"]["formatted"]

    if profile.has_key("bio"):
        profile_data["description"] = profile["bio"]

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

    for service_name in ["twitter", "facebook", "github"]:
        if profile.has_key(service_name):
            accounts.append(
                format_account(service_name, profile[service_name])
            )

    if profile.has_key("bitcoin") and type(profile["bitcoin"]) == dict and \
            profile["bitcoin"].has_key("address"):
        accounts.append({
            "@type": "Account",
            "role": "payment",
            "service": "bitcoin",
            "identifier": profile["bitcoin"]["address"]
        })

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

    profile_data["account"] = accounts 

    return profile_data


def convert_profile_to_legacy_format(profile_data):
    legacy_profile_data = {}

    if profile_data.get("name"):
        if isinstance(profile_data["name"], (str, unicode)):
            legacy_profile_data["name"] = {
                "formatted": profile_data["name"]
            }
        elif isinstance(profile_data["name"], dict):
            legacy_profile_data["name"] = profile_data["name"]

    if profile_data.get("address", {}).get("addressLocality"):
        legacy_profile_data["location"] = {
            "formatted": profile_data["address"]["addressLocality"]
        }

    if profile_data.get("website") and len(profile_data["website"]):
        website = profile_data["website"][0]
        if "url" in website:
            legacy_profile_data["website"] = website["url"]

    if profile_data.get("description"):
        legacy_profile_data["bio"] = profile_data["description"]

    if profile_data.get("image"):
        images = profile_data["image"]
        for image in images:
            if not ("name" in image and "contentUrl" in image):
                continue
            if image["name"] == "avatar":
                legacy_profile_data["avatar"] = {
                    "url": image["contentUrl"]
                }
            elif image["name"] == "cover":
                legacy_profile_data["cover"] = {
                    "url": image["contentUrl"]
                }

    if profile_data.get("account"):
        accounts = profile_data["account"]
        other_accounts = []
        for account in accounts:
            if not ("service" in account and "identifier" in account):
                continue
            old_account = {}
            if account["service"] in ["twitter", "facebook", "github"]:
                old_account = {"username": account["identifier"]}
            if account["service"] in ["bitcoin"]:
                old_account = {"address": account["identifier"]}
            if account["service"] in ["pgp"] and "contentUrl" in account:
                old_account = {"url": account["contentUrl"]}
                if "identifier" in account:
                    old_account["fingerprint"] = account["identifier"]

            if "proofUrl" in account:
                old_account["proof"] = {"url": account["proofUrl"]}

            if account["service"] == "twitter":
                legacy_profile_data["twitter"] = old_account
            elif account["service"] == "facebook":
                legacy_profile_data["facebook"] = old_account
            elif account["service"] == "github":
                legacy_profile_data["github"] = old_account
            elif account["service"] == "bitcoin":
                legacy_profile_data["bitcoin"] = old_account
            elif account["service"] == "pgp":
                legacy_profile_data["pgp"] = old_account
            else:
                other_accounts.append(account)
        if len(other_accounts):
            legacy_profile_data["account"] = other_accounts

    return legacy_profile_data
