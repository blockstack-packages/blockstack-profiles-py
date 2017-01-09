#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    blockstack-profiles-py
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016-2017 by Blockstack.org

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

import warlock

# sourced from https://github.com/blockstack/blockstack-profiles-js/blob/master/src/identities/person.es6 
PERSON_SCHEMA = {
  'type': 'object',
  'additionalProperties': True,
  'properties': {
    '@context': { 'type': 'string', 'optional': True },
    '@type': { 'type': 'string' },
    '@id': { 'type': 'string', 'optional': True },
    'name': { 'type': 'string', 'optional': True },
    'givenName': { 'type': 'string', 'optional': True },
    'familyName': { 'type': 'string', 'optional': True },
    'description': { 'type': 'string', 'optional': True },
    'image': {
      'type': 'array',
      'optional': True,
      'items': {
        'type': 'object',
        'properties': {
          '@type': { 'type': 'string' },
          'name': { 'type': 'string', 'optional': True },
          'contentUrl': { 'type': 'string', 'optional': True }
        }
      }
    },
    'website': {
      'type': 'array',
      'optional': True,
      'items': {
        'type': 'object',
        'properties': {
          '@type': { 'type': 'string' },
          'url': { 'type': 'string', 'optional': True }
        }
      }
    },
    'account': {
      'type': 'array',
      'optional': True,
      'items': {
        'type': 'object',
        'properties': {
          '@type': { 'type': 'string' },
          'service': { 'type': 'string', 'optional': True },
          'identifier': { 'type': 'string', 'optional': True },
          'proofType': { 'type': 'string', 'optional': True },
          'proofUrl': { 'type': 'string', 'optional': True },
          'proofMessage': { 'type': 'string', 'optional': True },
          'proofSignature': { 'type': 'string', 'optional': True }
        }
      }
    },
    'worksFor': {
      'type': 'array',
      'optional': True,
      'items': {
        'type': 'object',
        'properties': {
          '@type': { 'type': 'string' },
          '@id': { 'type': 'string', 'optional': True }
        }
      }
    },
    'knows': {
      'type': 'array',
      'optional': True,
      'items': {
        'type': 'object',
        'properties': {
          '@type': { 'type': 'string' },
          '@id': { 'type': 'string', 'optional': True }
        }
      }
    },
    'address': {
      'type': 'object',
      'optional': True,
      'properties': {
        '@type': { 'type': 'string' },
        'streetAddress': { 'type': 'string', 'optional': True },
        'addressLocality': { 'type': 'string', 'optional': True },
        'postalCode': { 'type': 'string', 'optional': True },
        'addressCountry': { 'type': 'string', 'optional': True }
      }
    },
    'birthDate': { 'type': 'string', 'optional': True },
    'taxID': { 'type': 'string', 'optional': True }
  },
}

Person = warlock.model_factory(PERSON_SCHEMA)
