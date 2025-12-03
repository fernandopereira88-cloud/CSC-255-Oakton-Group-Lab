def main():
    """Main entry for password management flow"""

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

if __name__ == "__main__":
    main()
