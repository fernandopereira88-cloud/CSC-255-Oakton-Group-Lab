"""
File used to generate user input for website name and password through command line.

Dependencies:
    click: command line interface
    pwinput: secure password input with visual feedback
"""

import click
import pwinput
from main import lookup_password_name, get_most_recent_password_names
from vigenere import decrypt


@click.command()
@click.option("--website", "-w", help="Website name")
@click.option("--password", "-p", help="Password", hide_input=True)
def keeper(website, password):
    """This is a command-line function."""

    greeting_msg = """
    Welcome to Keeper, a simple and secure solution for managing your credentials right from the command line!
    All you need to do is to provide website name and it's password.
    Keeper will encrypt your password using industry-standard protocols, ensuring your sensitive information remains 
    private and protected.
    """
    print(greeting_msg)

    if not website:
        website = click.prompt("Please enter the website name")

    while True:
        password = pwinput.pwinput(
            "Please enter the password (characters will show as *) : ", mask="*"
        )
        if not password:
            click.echo("Password cannot be empty.")
            continue

        confirm = pwinput.pwinput("Please confirm the password: ", mask="*")

        if password == confirm:
            break
        else:
            click.echo("Passwords do not match! Please try again.\n")

    click.echo(f"Credentials captured!")
    click.echo(f"Website: {website}")
    click.echo(f"Password: {'*' * len(password)}")

    #Menue loop
    while True:
        should_continue = print_menu()
        if not should_continue:
            break

    return website, password


def print_menu():
    """Print menu to show next step operations for user"""
    click.echo("\n" + "="*50)
    click.echo(f"What do you want to do next?")
    click.echo(f"1 - Retrieve password")
    click.echo(f"2 - Get recent saved password details")
    click.echo(f"3 - Exit")

    selection = click.prompt("Please enter your choice")
    return menu_execution(selection)


def menu_execution(selection):
    """Execute next step based on user input"""
    num = int(selection)

    if num == 1:
        website_name = click.prompt("Please enter the website name")
        result = lookup_password_name(website_name)
        if result: #lookup_pw returns encrypted pw, need to decrypte
            try:
                decrypted_pw = decrypt(result[0])
                click.echo(f"Website: {website_name}")
                click.echo(f"Password: {decrypted_pw}")
            except Exception as e:
                click.echo(f"Error decrypting passowrd: {e}")

    elif num == 2:
        get_most_recent_password_names()

    elif num == 3:
        click.echo("Thank you for using Keeper! Goodbye!")
        return False
    else:
        click.echo("Invalid selection. Please select a number from the menu")

    return True


if __name__ == "__main__":
    keeper()
