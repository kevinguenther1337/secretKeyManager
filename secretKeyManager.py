import random
import os
from cryptography.fernet import Fernet

# This script offers the option to create, remove, read, list or use keys for encryption / decryption.

# I can not guarantee for any form of secureness for the keys, it's just a test project.


# @return: Secret key or None if nothing has been found
def get_key(name: str, filename: str):
    if os.path.exists(filename) and os.stat(filename).st_size != 0 and name.upper() != "X":
        is_found = False
        key = ""
        with open(filename, "r+") as f:

            # Check if the key with the given name exists in the file
            for line in f.readlines():
                line_split = line.split(":")
                if line_split[0].lstrip().rstrip() == name:
                    is_found = True
                    key = line_split[1].rstrip().lstrip()
                    return key

            # If there is no key a new key gets generated with the given name
            if not is_found:
                return None

    # Generate new key if file is empty or doesn't exist
    else:
        with open(filename, "a") as f:
            key = Fernet.generate_key()
            f.write(f"{name} : " + key.decode() + "\n")

    return key.decode()


# Generates a random key and saves it to the file
def generate_key(name: str, filename: str):
    with open(filename, "a") as f:

        if get_key(name, filename) is None:
            key = Fernet.generate_key()
            f.write(f"{name} : " + key.decode() + "\n")

            print(f"\nGenerated key: {name}")
        else:
            print("\nKey does already exist!\nPlease try again with another name!")


# @return: Encrypted password
def encrypt(password: str, key: str):
    fernet = Fernet(key)
    message_encrypted = fernet.encrypt(password.encode())

    return f"\nPassword encrypted:\n{message_encrypted.decode()}\n"


# @return: Decrypted password
def decrypt(encrypted_text: str, key: str):
    fernet = Fernet(key)
    message_decrypted = fernet.decrypt(encrypted_text)

    return f"\nPassword decrypted:\n{message_decrypted.decode()}\n"


# @return: Returns a randomly generated password with desired length
# TODO: Build a password generator function
# ! NOT USED ATM !
def generate_password():
    password = []
    wanted_length = int(input("How long shall your password be?\n"))
    options = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
        "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "!", "§", "$", "%", "&", "=", "?", "#"]

    for _ in range(wanted_length):
        password.append(random.choice(options))
    print(''.join(password))
    return ''.join(password)


# Removes key from the given key storage file
def remove_key(filename: str):
    key_name = input("What is the name of the key?\n")

    is_found = False
    if key_name not in ["X", "x"]:
        with open(filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                line_split = line.split(":")

                if key_name in line_split[0]:
                    is_found = True
                    print("\nKey was successfully removed from the file!")
                    lines.remove(line)
                    break
            with open(filename, "w") as f:
                for line in lines:
                    f.write(line)

            if not is_found:
                print("\nThis key could not be found in this file!")
    else:
        print("\nStopped removing key..")


# Prints the menu of options for the user to choose from.
# @return: Returns the option the user choose from the menu
def menu():
    user_input = ""
    options = ["G", "S", "X", "N", "E", "D", "F", "R", "C"]
    while user_input not in options:
        print("\n==========( MENU )==========")
        print("F) Select file")
        print("S) Show available keys")
        print("G) Show key")
        print("R) Remove key")
        print("C) Create new key")
        print("E) Encrypt password with key")
        print("D) Decrypt password with key")
        print("X) Exit")
        print("============================\n")
        user_input = input("What do you want to do?\n").upper()
    return user_input


# Prints all the keys found in the given key file
def print_keys(filename: str):
    if os.path.exists(filename) and os.stat(filename).st_size != 0:
        with open(filename, "r") as f:
            print("==========(KEYS)==========")
            for line in f.readlines():
                if line != "" and line.find("========( KEYS )========") == -1 :
                    line_split = line.split(":")
                    print(line_split[0].lstrip().rstrip())
            print("==========================")

    else:
        print("No options available!")


# main with everything
def main():
    is_running = True
    filename = "!"
    fail_counter = 0  # Counts failed decryption attempts

    while is_running:

        # Delete file if there are to many failed inputs
        if fail_counter >= 3:  # Error count resets with restart of script
            print("\nDeleting key file because of too many failed inputs!")
            os.remove(filename)
            print("File succesfully deleted!")
            is_running = False
            user_input = "X"
        else:
            user_input = menu()

        # Exit the script
        if user_input == "X" and is_running:
            os.system("cls")
            is_running = not (user_input == "X" and is_running)

        # Get the filename
        elif user_input == "F":
            os.system("cls")
            filename = input("\nWhat is the name of the file?\n")

            print("\nFile succesfully selected!") if os.path.exists(filename) else \
                print("\nThis file could not be found!\n")

            if not os.path.exists(filename):
                if input("\nType (Y) to create this file or abort by typing something else!").upper() == "Y":
                    with open(filename, "w") as f:
                        f.write("========( KEYS )========\n")

        # Check if a file with the given name does exist
        elif is_running and not os.path.exists(filename) or filename == "!":
            os.system("cls")
            print("Please enter a filename!\n")

        # Prints list of all keys in the file
        elif user_input == "S":
            os.system("cls")
            print_keys(filename) if os.path.exists(filename) else print("\nThis file could not be found!")

        # Print key of given name
        elif user_input == "G":
            os.system("cls")

            key_name = input("What is the name of the key?\n")
            result_key = get_key(key_name, filename)
            print("\nThe key is:\n" + result_key) if result_key is None else print("\nThis key doesn't exist!")

        # Encrypt password with key
        elif user_input == "E":
            password = input("What is the password to encrypt?\n")
            key_name = input("What is the name of the key?\n")
            key = get_key(key_name, filename)

            if not key is None:
                password_encrypted = encrypt(password, key)
                print(password_encrypted)
            else:
                print("\nThis key could not be found!")

        # Decrypt password with key
        elif user_input == "D":
            os.system("cls")
            password_encrypted = input("What is the password to decrypt?\n").encode()
            key_name = input("What is the name of the key?\n")
            key = get_key(key_name, filename)

            if not key is None:
                password_decrypted = decrypt(password_encrypted, key)
                print(password_decrypted)
            else:
                print("\nThis key could not be found!\nPlease try again with the right key!")
                fail_counter += 1
                print(f"FAIL NR: {fail_counter}")
                if fail_counter == 2:
                    print("This is your last chance to get it right, or the file gets deleted!")

        # Remove a key from the key list
        elif user_input == "R":
            os.system("cls")
            remove_key(filename)

        # Create a new key
        elif user_input == "C":
            name = input("What is the name of the key?\n")
            generate_key(name, filename)


# Main part of script
main()
print("Stopping script..\n")
