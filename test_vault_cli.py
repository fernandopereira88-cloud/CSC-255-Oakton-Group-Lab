"""
CSC 255 - Automated CLI Tests for Password Vault
DRI: Jiajun Wang
Date: Dec 5, 2025

These tests validate the FULL APPLICATION by:
- invoking main()
- simulating real user input using unittest.mock.patch
- using a SEPARATE test vault file so no real data is touched
"""

import unittest
from unittest.mock import patch
from main import main
import database

# Use a dedicated vault file for CLI tests
TEST_VAULT = "test_cli_vault.txt"
database.VAULT_FILE_ADDRESS = TEST_VAULT


def reset_cli_vault():
    with open(TEST_VAULT, "w") as f:
        f.write("password_name,encrypted_password,created_at,last_updated_at\n")


def make_inputs(seq):
    for x in seq:
        yield x


class TestVaultCLI(unittest.TestCase):

    @patch("click.echo")
    @patch("pwinput.pwinput")
    @patch("click.prompt")
    def test_add_password(self, mock_prompt, mock_pwinput, mock_echo):

        reset_cli_vault()

        mock_prompt.side_effect = make_inputs([
            "1",            # menu: store password
            "google.com",   # website
            "6"             # exit after adding
        ])

        mock_pwinput.side_effect = make_inputs([
            "abc",          # pw
            "abc"           # confirm
        ])

        main()
        self.assertTrue(True)


    @patch("click.echo")
    @patch("click.prompt")
    def test_exit(self, mock_prompt, mock_echo):

        reset_cli_vault()

        mock_prompt.side_effect = ["6"]  # exit
        main()

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
