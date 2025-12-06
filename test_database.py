"""
CSC 255 - Automated Database Tests for Password Vault
DRI: Jiajun Wang
Date: Dec 5, 2025

This test suite verifies the correctness of low-level password storage
functions (NOT the CLI). These tests ensure that the vault file operations
behave correctly and that the database layer supports:

- create_password_name
- lookup_password_name
- update_password_name
- get_most_recent_password_names

These tests DO NOT simulate user input or test the CLI menu.
A separate test_vault_cli.py file will test the full main() application.
"""

import os
import time
from database import (
    create_password_name,
    lookup_password_name,
    update_password_name,
    get_most_recent_password_names,
)

TEST_VAULT = "test_vault.txt"


def reset_test_file():
    """Ensures an empty test vault file for each test."""
    with open(TEST_VAULT, "w") as f:
        f.write("password_name,encrypted_password,created_at,last_updated_at\n")
    import database
    database.VAULT_FILE_ADDRESS = TEST_VAULT


def test_create_password():
    reset_test_file()
    create_password_name("gmail", "abc123")

    result = lookup_password_name("gmail", privateCall=1)
    assert result == "abc123"
    print(" test_create_password passed")


def test_lookup_password():
    reset_test_file()
    create_password_name("github", "pass999")

    result = lookup_password_name("github", privateCall=1)
    assert result == "pass999"
    print(" test_lookup_password passed")


def test_update_password():
    reset_test_file()

    create_password_name("OaktonEmail", "oldpass")
    time.sleep(1)  
    update_password_name("OaktonEmail", "newpass")

    result = lookup_password_name("OaktonEmail", privateCall=1)
    assert result == "newpass"
    print(" test_update_password passed")


def test_top5_most_recent():
    reset_test_file()
    for i in range(1, 8):
        create_password_name(f"site{i}", f"pw{i}")
        time.sleep(0.1)

    print(" Running get_most_recent_password_names (no-crash test)")
    get_most_recent_password_names() 
    print(" test_top5_most_recent passed")


def run_all_tests():
    print("Running database tests...\n")

    test_create_password()
    test_lookup_password()
    test_update_password()
    test_top5_most_recent()

    print("\nALL TESTS PASSED ")


if __name__ == "__main__":
    run_all_tests()
