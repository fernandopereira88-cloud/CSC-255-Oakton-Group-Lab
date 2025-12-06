"""
CSC 255 - Automated CLI Tests for Password Vault
DRI: Jiajun Wang
Date: Dec 5, 2025

These tests verify ALL menu operations by calling main()
and simulating user input using unittest.mock.patch.

IMPORTANT:
- Tests DO NOT touch the real vault.txt
- Tests use a temporary vault file redirected via database.VAULT_FILE_ADDRESS
"""

import unittest
from unittest.mock import patch
import database
from main import main

TEST_VAULT = "test_cli_vault.txt"


def reset_cli_vault():
    """Prepare an isolated vault file for CLI tests."""
    with open(TEST_VAULT, "w") as f:
        f.write("password_name,encrypted_password,created_at,last_updated_at\n")

    database.VAULT_FILE_ADDRESS = TEST_VAULT


class TestVaultCLI(unittest.TestCase):

  
    # Test 1: CREATE PASSWORD

    @patch("click.echo")
    @patch("pwinput.pwinput")
    @patch("click.prompt")
    def test_cli_create(self, mock_prompt, mock_pwinput, mock_echo):
        reset_cli_vault()

        mock_prompt.side_effect = ["1", "gmail.com", "6"]
        mock_pwinput.side_effect = ["abc123", "abc123"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        stored = database.lookup_password_name("gmail.com", privateCall=1)
        self.assertIsNotNone(stored)


    # Test 2: RETRIEVE PASSWORD

    @patch("click.echo")
    @patch("click.prompt")
    def test_cli_retrieve(self, mock_prompt, mock_echo):
        reset_cli_vault()

        database.create_password_name("uiuc", "EncryptedPW")

        mock_prompt.side_effect = ["2", "uiuc", "6"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        called_strings = " ".join(str(c) for c in mock_echo.call_args_list)
        self.assertIn("Password retrieved successfully", called_strings)

   
    # Test 3: UPDATE PASSWORD
    
    @patch("click.echo")
    @patch("pwinput.pwinput")
    @patch("click.prompt")
    def test_cli_update(self, mock_prompt, mock_pwinput, mock_echo):
        reset_cli_vault()

        database.create_password_name("github", "OLD")

        mock_prompt.side_effect = ["3", "github", "6"]
        mock_pwinput.side_effect = ["NEWPASSWORD", "NEWPASSWORD"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        updated = database.lookup_password_name("github", privateCall=1)
        self.assertIsNotNone(updated)


    # Test 4: DELETE PASSWORD
  
    @patch("click.echo")
    @patch("pwinput.pwinput")
    @patch("click.prompt")
    def test_cli_delete(self, mock_prompt, mock_pwinput, mock_echo):
        reset_cli_vault()

        database.create_password_name("reddit", "AAA")

        mock_prompt.side_effect = ["4", "reddit", "6"]
        mock_pwinput.side_effect = ["AAA"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        result = database.lookup_password_name("reddit", privateCall=1)
        self.assertIsNone(result)

   
    # Test 5: RECENT LIST

    @patch("click.echo")
    @patch("click.prompt")
    def test_cli_recent(self, mock_prompt, mock_echo):
        reset_cli_vault()

        database.create_password_name("a", "1")
        database.create_password_name("b", "2")
        database.create_password_name("c", "3")

        mock_prompt.side_effect = ["5", "6"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        called = " ".join(str(c) for c in mock_echo.call_args_list)
        self.assertIn("TOP 5 MOST RECENTLY PASSWORD NAMES UPDATED", called)

    # Test 6: EXIT
    @patch("click.echo")
    @patch("click.prompt")
    def test_cli_exit(self, mock_prompt, mock_echo):
        reset_cli_vault()

        mock_prompt.side_effect = ["6"]

        with patch("builtins.input", side_effect=["6"]):
            try:
                main()
            except SystemExit:
                pass

        all_calls = " ".join(str(c) for c in mock_echo.call_args_list)
        self.assertIn("Goodbye", all_calls)


if __name__ == "__main__":
    unittest.main()
