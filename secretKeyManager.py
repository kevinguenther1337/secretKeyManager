import random
import os
from cryptography.fernet import Fernet

# This script does offer some ways to manage secret keys,
# its possible to generate & store keys for encryption and decryption,
# but also to just store the keys for other uses

# ! I can't guarante for total saveness of the keys, 
# it's only a "beginner" project! !


# @return: Secret key
def get_key(name: str, filename: str):
    if os.path.exists(filename) and os.stat(filename).st_size != 0 and name.upper() != "X":
        is_found = False
        key = ""
        with open(filename, "r+") as f:
            lines = f.readlines()

            # Check if the key with the given name exists in the file
            for line in lines:
                line_split = line.split(":")
                if line_split[0].lstrip().rstrip() == name:
                    is_found = True
                    key = line_split[1].rstrip().lstrip()
                    return key

            # If there is no key a new key gets generated with the given name
            if not is_found:
                key = Fernet.generate_key()
                f.write(f"{name} : " + key.decode() + "\n")

    # Generate new key if file is empty or doesn't exist
    else:
        with open(filename, "a") as f:
            key = Fernet.generate_key()
            f.write(f"{name} : " + key.decode() + "\n")

    return key.decode()


# @return: Encrypted password
def encrypt(password: str, key: str):
    fernet = Fernet(key)
    message_encrypted = fernet.encrypt(password.encode())

    return f"\nPassword encrypted\n{message_encrypted.decode()}\n"


# @return: Decrypted password
def decrypt(encrypted_text: str, key: str):
    fernet = Fernet(key)
    message_decrypted = fernet.decrypt(encrypted_text)

    return f"\nPassword decrypted:\n{message_decrypted.decode()}\n"


# @return: Returns a randomly generated password with desired length
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
    if key_name not in ["X","x"]:
        with open(filename, "r+") as f:
            lines = f.readlines()

            for line in lines:
                line_split = line.split(":")
                if key_name in line_split[0]:
                    is_found = True
                    print("Key was successfully removed!")
                    lines.remove(line)
                    break
            with open(filename, "w") as f:
                for line in lines:
                    f.write(line)

            if not is_found:
                print("This key doesn't exist!")
    else:
        print("Stopped removing..")


# Prints the menu of options for the user to choose from.
# @return: Returns the option the user choose from the menu
def menu():
    user_input = ""
    options = ["G", "S", "X", "N", "E", "D", "F", "R"]
    while user_input not in options:
        print("\n==========( MENU )==========")
        print("F) Select file")
        print("S) Show available keys")
        print("G) Get key or create new one")
        print("R) Remove key")
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
            lines = f.readlines()
            print("\n==========(KEYS)==========")
            for line in lines:
                if line != "" and line.find("=(KEYS)=") == -1 :
                    line_split = line.split(":")
                    print(line_split[0].lstrip().rstrip())
            print("==========================")

    else:
        print("No options available!")


def main():
    is_running = True
    filename = "!"

    while is_running:
        user_input = menu()

        if user_input == "X":  # Exit
            is_running = False

        elif user_input == "F":  # Get file name
            filename = input("\nWhat is the name of the file?\n")

            print("\nKey file does exist!") if os.path.exists(filename) else \
                print("\nKey file doesn't exist!\nPlease try again!\n")

            if not os.path.exists(filename):
                if input("Do you want to create this file? (Y)\n").upper() == "Y":
                    with open(filename, "w") as f:
                        f.write("====(KEYS)====\n")

        elif not os.path.exists(filename) or filename == "!":  # Check if filename is set
            print("Please enter a filename!\n")

        elif user_input == "S":  # Shows all names of possible keys
            print_keys(filename) if os.path.exists(filename) else print("File doesn't exist!")

        elif user_input == "G":  # Print key with given name
            print("If you want a new key, just enter a new name!")
            key_name = input("\nWhat is the key name?\n")
            print("\nThe key is:\n" + str(get_key(key_name, filename)))

        elif user_input == "E":  # Encrypt password
            password = input("What is the password to encrypt?\n")
            key_name = input("What is the name of the key?\n")
            key = get_key(key_name, filename)

            password_encrypted = encrypt(password, key)
            print(password_encrypted)

        elif user_input == "D":  # Decrypt password
            password_encrypted = input("What is the password to decrypt?\n").encode()
            key_name = input("What is the name of the key?\n")
            key = get_key(key_name, filename)

            password_decrypted = decrypt(password_encrypted, key)
            print(password_decrypted)

        elif user_input == "R":  # Remove key from file
            remove_key(filename)


main()
