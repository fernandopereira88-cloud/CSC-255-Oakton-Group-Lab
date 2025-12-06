import click
from cli_input import print_menu
import os
VAULT_FILE_ADDRESS = "vault.txt"

@click.command()
def main():
    """Main entry for password management flow"""

    greeting_msg = """
    Welcome to Keeper, a simple and secure solution for managing your credentials right from the command line!
    All you need to do is to provide website name and it's password.
    Keeper will encrypt your password using industry-standard protocols, ensuring your sensitive information remains 
    private and protected.
    """
    click.echo(greeting_msg)

    # Check if a vault already exists. If a vault does not exists, create one.
    if not os.path.exists(VAULT_FILE_ADDRESS):
        with open(VAULT_FILE_ADDRESS, "w") as file:
            data = "password_name,encrypted_password,created_at,last_updated_at\n"
            file.write(data)
                
    while True:
        should_continue = print_menu()
        if not should_continue:
            break


if __name__ == "__main__":
    main()
