#!/usr/bin/env python

"""Tests for `local_keychain_utils` package."""

# from local_keychain_utils import local_keychain_utils
import os
import subprocess
import sys

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cli_get_help():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """usage: local-keychain-get [-h] [--backend [BACKEND]] service username

Retrieve a secret in local keychain

positional arguments:
  service              service to log into (e.g., URL)
  username             Username to use

options:
  -h, --help           show this help message and exit
  --backend [BACKEND]  Keyring backend to use
"""
    if sys.version_info <= (3, 10):
        # 3.10 changed the wording a bit
        expected_help = expected_help.replace('options:', 'optional arguments:')

    actual_help = subprocess.check_output(['local-keychain-get', '--help'],
                                          env=env).decode('utf-8')
    assert actual_help == expected_help
