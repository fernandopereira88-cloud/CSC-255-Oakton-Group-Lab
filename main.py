import click
from cli_input import print_menu


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

    while True:
        should_continue = print_menu()
        if not should_continue:
            break


if __name__ == "__main__":
    main()
