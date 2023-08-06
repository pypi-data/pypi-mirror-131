#!/usr/bin/env python3

import argparse

import keyring
from keyring import core


def main() -> None:
    desc = 'Remove a secret in local keychain'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--backend', type=str, nargs='?',
                        help='Keyring backend to use')
    parser.add_argument('service', type=str,
                        help='service to log into (e.g., URL)')
    parser.add_argument('username', type=str,
                        help='Username to use')

    args: argparse.Namespace = parser.parse_args()
    service: str = args.service
    username: str = args.username
    backend: str = args.backend

    if backend is not None:
        keyring.set_keyring(core.load_keyring(backend))
    keyring.delete_password(service, username)
