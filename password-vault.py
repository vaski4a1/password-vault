import os
import json

def main():
    print("                                  Welcome to vaski4a's Password Saver")
    print()
    print("1. Add Password")
    print("2. Delete Password")
    print("3. Update Password")
    print("[Q] Exit the tool")
    print()
    choice = input("Choose an option: ").lower()

    if choice == '1':
        add_password()
    elif choice == '2':
        delete_password()
    elif choice == '3':
        update_password()
    elif choice == 'q':
        exit()
    else:
        print("Invalid choice. Try again.")
        main()

def add_password():
    name = input("App/Website name: ")
    email = input("Email: ")
    password = input("Password: ")

    # Validate email
    if '@' not in email or '.' not in email:
        print("Invalid email format. Please try again.")
        return add_password()

    # Load or initialize vault
    data = {"next_id": 1, "entries": []}
    if os.path.exists("vault.json"):
        with open("vault.json", "r") as f:
            try:
                loaded = json.load(f)
                if "entries" in loaded and "next_id" in loaded:
                    data = loaded
            except json.decoder.JSONDecodeError:
                print("Vault corrupted, starting fresh.")

    # Create new entry
    new_entry = {
        "id": data["next_id"],
        "website": name,
        "email": email,
        "password": password,
    }

    data["entries"].append(new_entry)
    data["next_id"] += 1

    # Save updated vault
    with open("vault.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Password successfully saved. ID: {new_entry['id']}")
    
    goback = input("Press [M] to go to the main menu: ").upper()
    if goback == "M":
        main()

def delete_password():
    if not os.path.exists("vault.json"):
        print("Vault file not found. Nothing to delete.")
        return

    with open("vault.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Vault is corrupted or empty.")
            return

    if not data.get("entries"):
        print("No saved passwords to delete.")
        return

    print("\nSaved Passwords:")
    for entry in data["entries"]:
        print(f"ID: {entry['id']} | Site: {entry['website']} | Email: {entry['email']}")
    print("-" * 40)

    try:
        delete_id = int(input("Enter the ID of the password to delete: "))
    except ValueError:
        print("Invalid ID. Must be a number.")
        return

    # Check if ID exists
    found = False
    new_entries = []
    for entry in data["entries"]:
        if entry["id"] == delete_id:
            found = True
            continue
        new_entries.append(entry)

    if not found:
        print(f"No password found with ID {delete_id}.")
        return

    data["entries"] = new_entries

    with open("vault.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Password with ID {delete_id} deleted successfully.")

    goback = input("Press [M] to go back to the main menu: ").upper()
    if goback == "M":
        main()


def update_password():
    if not os.path.exists("vault.json"):
        print("Vault file not found.")
        return

    with open("vault.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Vault is corrupted.")
            return

    if not data.get("entries"):
        print("No saved passwords to update.")
        return

    print("\n📂 Saved Passwords:")
    for entry in data["entries"]:
        print(f"ID: {entry['id']} | Site: {entry['website']} | Email: {entry['email']}")
    print("-" * 40)

    try:
        update_id = int(input("Enter the ID of the password to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for entry in data["entries"]:
        if entry["id"] == update_id:
            print("\nLeave input empty if you don’t want to change that field.")

            new_site = input(f"New site (current: {entry['website']}): ")
            new_email = input(f"New email (current: {entry['email']}): ")
            new_password = input(f"New password (current: {entry['password']}): ")

            if new_site.strip() != "":
                entry["website"] = new_site
            if new_email.strip() != "":
                entry["email"] = new_email
            if new_password.strip() != "":
                entry["password"] = new_password

            with open("vault.json", "w") as f:
                json.dump(data, f, indent=2)

            print("Data updated successfully.")
            break
    else:
        print(f"No password found with ID {update_id}.")

    goback = input("Press [M] to go back to the main menu: ").upper()
    if goback == "M":
        main()


if __name__ == "__main__":
    main()
