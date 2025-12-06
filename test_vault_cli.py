import click
import pwinput
import database as db
import unittest
from unittest.mock import patch

def print_welcome():
    click.echo("""
    Welcome to Keeper, a simple and secure solution for managing your credentials!
    """)

def print_menu():
    click.echo("\n==================================================")
    click.echo("Please select from the following menu: ")
    click.echo("1 - Store a new password")
    click.echo("2 - Retrieve a stored password")
    click.echo("3 - Update a stored password")
    click.echo("4 - Delete a stored password")
    click.echo("5 - Get recent password")
    click.echo("6 - Exit")
    click.echo("==================================================")
    selection = click.prompt("", type=str)
    return menu_execution(selection)


def menu_execution(selection):

    # CREATE
    if selection == "1":
        site = click.prompt("Enter website")
        pw1 = pwinput.pwinput("Enter password: ", mask="*")
        pw2 = pwinput.pwinput("Confirm password: ", mask="*")

        if pw1 != pw2:
            click.echo("Passwords do not match.")
            return True
        
        db.create_password_name(site, pw1)
        click.echo(f"Password stored successfully for {site}")
        return True

    # RETRIEVE
    elif selection == "2":
        site = click.prompt("Enter website")
        encrypted = db.lookup_password_name(site)

        if encrypted is None:
            click.echo("No password found for this website.")
        else:
            decrypted = db.decrypt_password(encrypted)   # ★★★ FIX ★★★
            click.echo("Password retrieved successfully")
            click.echo(f"The password for {site} is {decrypted}")

        return True

    # UPDATE
    elif selection == "3":
        site = click.prompt("Enter website")
        new_pw = pwinput.pwinput("Enter new password: ", mask="*")

        db.update_password_name(site, new_pw)
        click.echo(f"Password for {site} successfully updated")
        return True

    # DELETE
    elif selection == "4":
        site = click.prompt("Enter website")
        pw = pwinput.pwinput("Enter password to delete: ", mask="*")

        success = db.delete_password_name(site, pw)

        if success:
            click.echo(f"Password for {site} successfully deleted.")
        else:
            click.echo("CANNOT DELETE PASSWORD. Wrong password entered.")
        return True

    # RECENT
    elif selection == "5":
        click.echo("PASSWORD NAMES REPORT")
        db.get_most_recent_password_names()
        return True

    # EXIT
    elif selection == "6":
        click.echo("Thank you for using Keeper! Goodbye!")
        return False

    else:
        click.echo("Invalid selection.")
        return True


class MenuExecutionTests(unittest.TestCase):
    def test_store_password_success(self):
        with patch("test_vault_cli.click.prompt", return_value="github"), patch(
            "test_vault_cli.pwinput.pwinput", side_effect=["pw123", "pw123"]
        ), patch("test_vault_cli.db.create_password_name") as create_mock, patch(
            "test_vault_cli.click.echo"
        ):
            result = menu_execution("1")

        self.assertTrue(result)
        create_mock.assert_called_once_with("github", "pw123")
        print("test_store_password_success PASSED")

    def test_store_password_mismatch(self):
        with patch("test_vault_cli.click.prompt", return_value="gmail"), patch(
            "test_vault_cli.pwinput.pwinput", side_effect=["a", "b"]
        ), patch("test_vault_cli.click.echo") as echo_mock, patch(
            "test_vault_cli.db.create_password_name"
        ) as create_mock:
            result = menu_execution("1")

        self.assertTrue(result)
        create_mock.assert_not_called()
        echo_mock.assert_any_call("Passwords do not match.")
        print("test_store_password_mismatch PASSED")

    def test_retrieve_password_found(self):
        with patch("test_vault_cli.click.prompt", return_value="github"), patch(
            "test_vault_cli.db.lookup_password_name", return_value="encrypted"
        ), patch(
            "test_vault_cli.db.decrypt_password",
            return_value="plaintext",
            create=True,
        ), patch("test_vault_cli.click.echo") as echo_mock:
            result = menu_execution("2")

        self.assertTrue(result)
        echo_mock.assert_any_call("Password retrieved successfully")
        echo_mock.assert_any_call("The password for github is plaintext")
        print("test_retrieve_password_found PASSED")

    def test_retrieve_password_missing(self):
        with patch("test_vault_cli.click.prompt", return_value="github"), patch(
            "test_vault_cli.db.lookup_password_name", return_value=None
        ), patch("test_vault_cli.click.echo") as echo_mock:
            result = menu_execution("2")

        self.assertTrue(result)
        echo_mock.assert_any_call("No password found for this website.")
        print("test_retrieve_password_missing PASSED")

    def test_exit_option(self):
        with patch("test_vault_cli.click.echo"):
            result = menu_execution("6")
        self.assertFalse(result)
        print("test_exit_option PASSED")


def run_cli():
    """Simple runner so the module can be executed directly during ad-hoc testing."""
    print_welcome()
    while True:
        should_continue = print_menu()
        if not should_continue:
            break


if __name__ == "__main__":
    run_cli()
