import json
import os
import sys
import re
import unittest

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ta_linode_util'))


def request_url_to_fixture(url: str):
    """Convert a URL path to a fixtures filename ('/account/events' -> 'account_events')"""
    return '_'.join([param for param in re.split('/|-', url) if param != ''])


def request_fixture_override(handler, fixtures_dir=FIXTURES_DIR):
    """Override the request methods in a handler with file-based fixtures"""

    def f(url, *args, **kwargs):
        fixture_name = '{}.json'.format(request_url_to_fixture(url))
        fixture_path = os.path.join(fixtures_dir, fixture_name)

        return load_fixture(fixture_path)

    handler._get = f


def request_fixture_override_func(handler, func):
    """Override the request methods in a handler with a custom handler func"""

    def f(url, *args, **kwargs):
        return func('get', url, *args, **kwargs)

    handler._get = f


def load_fixture(fixture_path):
    """Load a fixture from the given file"""

    with open(fixture_path) as f:
        content = f.read()

    return json.loads(content)
