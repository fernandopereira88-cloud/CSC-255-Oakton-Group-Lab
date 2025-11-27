"""
File used to generate user input for website name and password through command line.

Dependencies:
    click: command line interface
    pwinput: secure password input with visual feedback
"""

import click
import pwinput


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

    return website, password


if __name__ == "__main__":
    keeper()
