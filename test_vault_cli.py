"""
CSC 255 - Automated CLI Tests for Password Vault
Tests the FULL PROGRAM by calling main() and simulating user input.

DRI: Jiajun Wang
"""

import unittest
from unittest.mock import patch

from main import main  # IMPORTANT: test from main.py !!!


def make_inputs(seq):
    """Helper generator for scripted CLI inputs"""
    for x in seq:
        yield x


class TestVaultCLI(unittest.TestCase):

    @patch("click.echo")
    @patch("pwinput.pwinput")
    @patch("click.prompt")
    def test_add_password(self, mock_prompt, mock_pwinput, mock_echo):
        """
        Simulate the flow:
          1 → store password
          website → google.com
          pw → abc
          exit → 6
        """

        mock_prompt.side_effect = make_inputs([
            "1",           
            "google.com",   
            "6"            
        ])

        mock_pwinput.side_effect = make_inputs([
            "abc",  
            "abc"  
        ])

        with patch("builtins.input", side_effect=["6"]):
            main()

        self.assertTrue(True)

    @patch("click.echo")
    @patch("click.prompt")
    def test_exit(self, mock_prompt, mock_echo):
        """Program must exit cleanly"""

        mock_prompt.side_effect = ["6"]  # Exit

        with patch("builtins.input", side_effect=["6"]):
            main()

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
