"""
File used to generate user input for website name and password through command line.

Dependencies:
    click: command line interface
    pwinput: secure password input with visual feedback
"""

import click
import pwinput
import database as db
from vigenere import decrypt, encrypt


def print_menu():
    """Print menu to show next step operations for user"""
    click.echo("\n" + "="*50)
    click.echo(f"Please select from the following menu: ")
    click.echo(f"1 - Store a new password")
    click.echo(f"2 - Retrieve a stored password")
    click.echo(f"3 - Update a stored password")
    click.echo(f"4 - Delete a stored password")
    click.echo(f"5 - Get recent password")
    click.echo(f"6 - Exit")

    selection = click.prompt("Please enter your choice")
    return menu_execution(selection)


def keeper(add=True):
    """Interact with user to get website name and password"""
    if add is True:
        website = click.prompt("Please enter the website name")
    else:
        website = click.prompt("Please enter the website name you want to update")

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

    #Encrypt the pw
    encrypted_pw = encrypt(password)
    if add is True:
        #Save pw
        db.create_password_name(website, encrypted_pw)
    else:
        #Update pw
        db.update_password_name(website, encrypted_pw)

    #Confirm user input
    click.echo(f"Credentials captured!")
    click.echo(f"Website: {website}")
    click.echo(f"Password: {'*' * len(password)}")

    return website, password


@click.command()

def main():
    """This is a command-line function."""

    greeting_msg = """
    Welcome to Keeper, a simple and secure solution for managing your credentials right from the command line!
    All you need to do is to provide website name and it's password.
    Keeper will encrypt your password using industry-standard protocols, ensuring your sensitive information remains 
    private and protected.
    """
    click.echo(greeting_msg)

    while True:
        should_continue = print_menu()
        if not should_continue:
            break






def menu_execution(selection):
    """Execute next step based on user input"""
    try:
        num = int(selection)
    except ValueError:
        return "Invalid selection. Please select a number from the menu"

    if num == 1: #save new pw
       keeper(add = True)

    elif num == 2: #get pw
        website_name = click.prompt("Please enter the website name")
        result = db.lookup_password_name(website_name)
        if result:
            try:
                decrypted_pw = decrypt(result[0])
                click.echo(f"Password retrieved successfully!")
                click.echo(f"Website: {website_name}")
                click.echo(f"Password: {decrypted_pw}")
            except Exception as e:
                click.echo(f"Error decrypting password: {e}")

    elif num == 3: #update
        keeper(add=False)

    elif num == 4: #delete
        website4 = click.prompt("Please enter the website name you want to delete")
        pw4 = pwinput.pwinput("Please enter the password (characters will show as *) : ", mask="*")
        encrypted_pw4 = encrypt(pw4)
        db.delete_password_name(website4, encrypted_pw4)

    elif num == 5: #get recent
        db.get_most_recent_password_names()

    elif num == 6: #exit
        click.echo("Thank you for using Keeper! Goodbye!")
        return False

    else:
        click.echo("Invalid selection. Please selection 1-6")

    return True


if __name__ == "__main__":
    main()
