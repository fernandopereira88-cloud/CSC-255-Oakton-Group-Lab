import time
from datetime import datetime
import os
from goodrich.ch10.probe_hash_map import ProbeHashMap as phm
from goodrich.ch09.max_heap_priority_queue_pereira import MaxHeapPriorityQueue as mpq
from vigenere import decrypt, encrypt
import pwinput

VAULT_FILE_ADDRESS = "vault.txt"

def check_database():
    # Check if a vault already exists. If a vault does not exists, create one.
    if not os.path.exists(VAULT_FILE_ADDRESS):
        with open(VAULT_FILE_ADDRESS, "w") as file:
            data = "password_name,encrypted_password,created_at,last_updated_at\n"
            file.write(data)
            
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
        print("\nNo password vault has been found. Create a password first.")
        return

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
            print(f"\nThe password NAME {name} was not found in order to be updated.")
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
    if not os.path.exists(VAULT_FILE_ADDRESS):
        # Password is actually a new password, because there is no vault.txt file. So call create_password() instead.
        print("No password vault has been found. Create a password first.")
        return

    # Check if the password name exists
    passSearch = lookup_password_name(name, privateCall=1)
    if passSearch == False:
        print(
            f"\nThe password NAME {name} does not exist and cannot be deleted. Try another password name."
        )
        return False

    # Confirm password before deleting
    while passSearch != pwd:
        print(
            "\nCANNOT DELETE PASSWORD. Wrong password entered. Try again, or type 'EXIT' to go back to the main menu."
        )

        pwd = pwinput.pwinput("Enter the password: ", mask="*")
        if pwd.lower() == "exit":
            return
        else:
            pwd = encrypt(pwd)

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
    Description: function to create a new password

    Inputs:
        - name: the password name with the encrypted password to be retrieved
        - privateCall: set to 0 by default and will return a message to the user when the password name is not found.
                       If set to 1, there will be no such message. Set it to 1 when calling lookup_password_name() within the app
    Outputs:
        - A tuple with the encrypted (password,createAt,lastUpdatedAt)
    """
    if not os.path.exists(VAULT_FILE_ADDRESS):
        # Password is actually a new password, because there is no vault.txt file. So call create_password() instead.
        print("\nNo password vault has been found. Create a password first.")
        return

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

        else:
            return False
    else:
        if privateCall == 0:
            return print(f"The password for {name} is {decrypt(lookupValue)}")
        else:
            return lookupValue


def get_most_recent_password_names():
    """
    Description: Display the top 5 most recently updated password names
    Inputs: None
    Outputs: Prints the top 5 most recently updated entries
    """

    # FIX: Add this check at the beginning
    if not os.path.exists(VAULT_FILE_ADDRESS):
        print("\n📭 Your vault is empty!")
        print("   Start by creating your first password entry.\n")
        return

    mostRecentUpdatedPasswordNameHeap = mpq()

    try:
        with open(VAULT_FILE_ADDRESS, "r") as file:
            # Check if file has data beyond header
            has_data = False
            for line in file:
                fields = line.rstrip().split(",")
                if fields[0] != "password_name":
                    has_data = True
                    mostRecentUpdatedPasswordNameHeap.add(fields[3], fields[0])

            # FIX: Check if we found any data
            if not has_data:
                print("\n📭 Your vault is empty!")
                print("   Start by creating your first password entry.\n")
                return

    except FileNotFoundError:
        print("\n📭 Your vault is empty!")
        print("   Start by creating your first password entry.\n")
        return

    # Rest of the function remains the same...
    index = 1
    print("==============================================================")
    print("= PASSWORD NAMES REPORT (ORDERED BY CREATION TIME DESCENDING =")
    print("==============================================================")
    print("# | Password name\t| Most Recent Update\t\t|")
    print("_________________________________________________________")

    while not mostRecentUpdatedPasswordNameHeap.is_empty():
        item = mostRecentUpdatedPasswordNameHeap.remove_max()
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
