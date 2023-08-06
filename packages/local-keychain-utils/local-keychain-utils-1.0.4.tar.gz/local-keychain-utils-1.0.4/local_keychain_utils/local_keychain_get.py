#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace

import keyring
from keyring import core


def main():
    parser: ArgumentParser =\
        ArgumentParser(description='Retrieve a secret in local keychain')

    parser.add_argument('--backend', type=str, nargs='?',
                        help='Keyring backend to use')
    parser.add_argument('service', type=str,
                        help='service to log into (e.g., URL)')
    parser.add_argument('username', type=str,
                        help='Username to use')

    args: Namespace = parser.parse_args()
    service: str = args.service
    username: str = args.username
    backend: str = args.backend

    if backend is not None:
        keyring.set_keyring(core.load_keyring(backend))
    password: str = keyring.get_password(service, username)
    if password is None:
        exit(1)
    else:
        print(password)
