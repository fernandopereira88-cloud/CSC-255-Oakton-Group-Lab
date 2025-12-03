from vigenere import decrypt, encrypt

import time
from datetime import datetime
import os
from goodrich.ch10.probe_hash_map import ProbeHashMap as phm
from goodrich.ch09.max_heap_priority_queue_pereira import MaxHeapPriorityQueue as mpq
import click
import pwinput

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

    #Encrypt the pw
    encrypted_pw = encrypt(password)
    if add is True:
        #Save pw
        create_password_name(website, encrypted_pw)
    else:
        #Update pw
        update_password_name(website, encrypted_pw)

    #Confirm user input
    click.echo(f"Credentials captured!")
    click.echo(f"Website: {website}")
    click.echo(f"Password: {'*' * len(password)}")

    return website, password


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
        result = lookup_password_name(website_name)
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
        delete_password_name(website4, encrypted_pw4)

    elif num == 5: #get recent
        get_most_recent_password_names()

    elif num == 6: #exit
        click.echo("Thank you for using Keeper! Goodbye!")
        return False

    else:
        click.echo("Invalid selection. Please selection 1-6")

    return True


def create_password_name(name, pwd):
    """
    Description: function to create a new password

    Inputs:
        - name: the password name
        - pwd: the encrypted password to be stored in the file database
    Outputs:
        - A print confirming that the password was stored
    """

    if not os.path.exists(VAULT_FILE_ADDRESS):
        with open(VAULT_FILE_ADDRESS, "w") as file:
            data = "password_name,encrypted_password,created_at,last_updated_at\n"
            createAt = str(time.time())
            lastUpdatedAt = str(time.time())
            data += name + "," + pwd + "," + createAt + "," + lastUpdatedAt + "\n"
            file.write(data)
    else:

        if lookup_password_name(name, privateCall=1):
            print(
                f"\nThe password NAME {name} already has a password assigned. Use the update function to set a new password."
            )
            return False

        with open(VAULT_FILE_ADDRESS, "a") as file:
            createAt = str(time.time())
            lastUpdatedAt = str(time.time())
            data = name + "," + pwd + "," + createAt + "," + lastUpdatedAt + "\n"
            file.write(data)

    print(f"\nPassword stored successfully for {name}")


def update_password_name(name, pwd):
    """
    Description: function to create a new password

    Inputs:
        - name: the password name with the encrypted password to be retrieved
        - pwd: the NEW encrypted password to be stored in the file database
    Outputs:
        - A print confirming that the password was stored
    """
    if not os.path.exists(VAULT_FILE_ADDRESS):
        # Password is actually a new password, because there is no vault.txt file. So call create_password() instead.
        return create_password_name(name=name, pwd=pwd)

    else:
        # Read file
        updateRow = 0
        newContentLine = ""
        with open(VAULT_FILE_ADDRESS, "r") as readFile:
            contentLines = readFile.readlines()

        for index in range(len(contentLines)):
            contentSplit = contentLines[index].rstrip().split(",")
            if contentSplit[0] == name:
                newLastUpdatedAt = str(time.time())
                newContentLine = (
                    contentSplit[0]
                    + ","
                    + pwd
                    + ","
                    + contentSplit[2]
                    + ","
                    + newLastUpdatedAt
                )
                updateRow = index
                break

        if newContentLine == "":
            print("\nThe password NAME {name} was not found in order to be updated.")
        else:
            contentLines[updateRow] = newContentLine + "\n"

            with open(VAULT_FILE_ADDRESS, "w") as writeFile:
                writeFile.writelines(contentLines)
                print(f"\nPassword for {name} succesfully updated")


def delete_password_name(name, pwd):
    """
    Description: function to create a new password

    Inputs:
        - name: the password name with the encrypted password to be deleted
        - pwd: the encrypted password provided as confirmation that it is OK to delet
    Outputs:
        - A print confirming that the password was deleted
    """
    while lookup_password_name(name) != pwd:
        print(
            "\nCANNOT DELETE PASSWORD. Wrong password entered. Try again, or type 'EXIT' to go back to the main menu."
        )
        pwd = input("Enter the password:")
        if pwd.lower() == "exit":
            return

    deleteRow = 0
    newContentLine = ""

    with open(VAULT_FILE_ADDRESS, "r") as readFile:
        contentLines = readFile.readlines()
    newContentLines = [line for line in contentLines if name not in line]

    with open(VAULT_FILE_ADDRESS, "w") as writeFile:
        writeFile.writelines(newContentLines)
        print(f"\nPassword for {name} succesfully deleted.")


def lookup_password_name(name, privateCall=0):
    """
    Description: function to look up a password

    Inputs:
        - name: the password name with the encrypted password to be retrieved
        - privateCall: set to 0 by default and will return a message to the user when the password name is not found.
                       If set to 1, there will be no such message. Set it to 1 when calling lookup_password_name() within the app
    Outputs:
        - The encrypted password string
    """
    lookUpHashTable = phm(
        cap=1231, probingMethod="double"
    )  # Instantiate a Hash Table using double hashing to store and lookup the name

    with open(VAULT_FILE_ADDRESS, "r") as file:
        for line in file:
            fields = line.rstrip().split(",")
            lookUpHashTable[fields[0]] = fields[
                1
            ]  # fields[0] --> password name // fields[1] --> password

    lookupValue = lookUpHashTable[
        name
    ]  # the encrypted password. Use lookUpHashTable[name] to return more data points such as created date and updated date
    if not lookupValue:
        if privateCall == 0:
            return print(
                f"\nPassword name {name} not found. Please, create a new password name for this name to be able to use it."
            )

        return False
    else:
        if privateCall == 0:
            print(f"The password for {name} is {lookupValue}")
        return lookupValue


def get_most_recent_password_names():
    """
    Description:
    Inputs:
        -
    Outputs:
        -
    """
    mostRecentUpdatedPasswordNameHeap = mpq()
    with open(VAULT_FILE_ADDRESS, "r") as file:
        for line in file:
            fields = line.rstrip().split(",")
            if fields[0] != "password_name":
                mostRecentUpdatedPasswordNameHeap.add(
                    fields[3], fields[0]
                )  # fields[3] --> Most Recent Updated At || fields[0] --> Password Name

    index = 1
    print("=========================================================")
    print("= TOP 5 MOST RECENTLY PASSWORD NAMES UPDATED            =")
    print("=========================================================")
    print("# | Password name\t| Most Recent Update\t\t|")
    print("_________________________________________________________")
    while mostRecentUpdatedPasswordNameHeap.is_empty() == False and index <= 5:
        item = mostRecentUpdatedPasswordNameHeap.remove_max()
        passwordName = item[1]
        itemFormattedTime = datetime.fromtimestamp(float(item[0]))
        print(index, "|", item[1], "\t|", itemFormattedTime, "\t|")
        index += 1
    print("_________________________________________________________")


def test():
    # Test: Create new password names
    create_password_name("FernandoEmail", "1234")
    create_password_name("AudreyHomeWifi", "5678")
    create_password_name("QuangKindle", "abcde")

    # Test: Create new password name for a password name that already exists
    create_password_name("FernandoEmail", "1234")

    # Test: Password name doesn't exist
    lookup_password_name(
        "TemesvariOakton"
    )  # Need to find a way to print this accordingly. Currenlty only printing "False"

    # Test: Update password name
    lookup_password_name("FernandoEmail")
    update_password_name("FernandoEmail", "Roll!")
    lookup_password_name("FernandoEmail")

    # Test: Delete password name
    # delete_password_name("QuangKindle","1234")

    # Test:Get the most recent password updated on the database
    get_most_recent_password_names()


if __name__ == "__main__":
    test()
