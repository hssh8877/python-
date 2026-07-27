import argparse
import hashlib
import json
import os

MASTER_FILE = "master.json"
PASSWORDS_FILE = "passwords.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def set_master_password():
    master = input("Set a master password: ")
    hashed = hash_password(master)

    with open(MASTER_FILE, "w") as f:
        json.dump({"master": hashed}, f)

    print("Master password set.")

def verify_master_password():
    if not os.path.exists(MASTER_FILE):
        print("No master password set. Run 'set-master' first.")
        return False

    with open(MASTER_FILE, "r") as f:
        data = json.load(f)

    stored_hash = data["master"]

    attempt = input("Enter master password: ")
    attempt_hash = hash_password(attempt)

    if attempt_hash == stored_hash:
        print("Access granted.")
        return True
    else:
        print("Access denied.")
        return False

def load_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r") as f:
        return json.load(f)

def save_passwords(data: dict):
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_password(name: str, password: str):
    passwords = load_passwords()

    if name in passwords:
        print(f"{name} already exists.")
        return

    passwords[name] = password
    save_passwords(passwords)
    print(f"Password for {name} added.")

def get_password(name: str):
    passwords = load_passwords()

    if name not in passwords:
        print(f"No password stored for {name}")
        return

    print(f"{name}: {passwords[name]}")

def delete_password(name: str):
    passwords = load_passwords()

    if name not in passwords:
        print(f"No password stored for {name}")
        return

    del passwords[name]
    save_passwords(passwords)
    print(f"Password for {name} deleted.")

def list_passwords():
    passwords = load_passwords()

    if not passwords:
        print("No passwords stored.")
        return

    for name in passwords:
        print(name)

def main():
    parser = argparse.ArgumentParser(description="Password Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new password")
    add_parser.add_argument("name", help="Name of the service")
    add_parser.add_argument("password", help="Password for the service")

    get_parser = subparsers.add_parser("get", help="Get a stored password")
    get_parser.add_argument("name", help="Name of the service")

    delete_parser = subparsers.add_parser("delete", help="Delete a stored password")
    delete_parser.add_argument("name", help="Name of the service")

    subparsers.add_parser("list", help="List all stored passwords")
    subparsers.add_parser("set-master", help="Set a master password")

    args = parser.parse_args()

    if args.command == "set-master":
        set_master_password()

    elif args.command in ["add", "get", "delete", "list"]:
        if not verify_master_password():
            return

        if args.command == "add":
            add_password(args.name, args.password)
        elif args.command == "get":
            get_password(args.name)
        elif args.command == "delete":
            delete_password(args.name)
        elif args.command == "list":
            list_passwords()

if __name__ == "__main__":
    main()
