import os
import shutil
import json
from datetime import datetime
language = "it"
from config import destinations, patterns

CONFIG_FILE = 'config.py'

def log_action(action):
    log_folder = os.path.join(os.getcwd(), 'DPLOG')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, 'log.json')

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action
    }

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(log_entry)

    with open(log_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def show_log():
    log_file_path = os.path.join(os.getcwd(), 'DPLOG', 'log.json')

    if not os.path.exists(log_file_path):
        print("No log found.")
        return

    with open(log_file_path, 'r') as file:
        data = json.load(file)

    if not data:
        print("The log is empty.")
        return

    for entry in data:
        print(f"{entry['timestamp']}: {entry['action']}")

def save_config_to_file():
    config_content = (
        f"destinations = {json.dumps(destinations, indent=4)}\n\n"
        f"patterns = {json.dumps(patterns, indent=4)}\n"
    )
    with open(CONFIG_FILE, 'w') as file:
        file.write(config_content)

class FileOrganizer:
    def __init__(self, source_folder=None):
        if source_folder is None:
            self.source_folder = self.get_source_folder()
        else:
            self.source_folder = source_folder

        self.destinations = destinations

    def get_source_folder(self):
        current_dir = os.getcwd()
        return current_dir

    def create_destination_folders(self, folders):
        for folder in folders:
            folder_path = os.path.join(self.source_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_file(self, filename, folder):
        file_path = os.path.join(self.source_folder, filename)
        destination_path = os.path.join(self.source_folder, folder, filename)
        shutil.move(file_path, destination_path)
        print(f"Moved: {filename} -> {folder}")
        log_action(f"Moved file: {filename} to {folder}")

    def organize(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(self.destinations.keys())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            _, extension = os.path.splitext(filename)
            for folder, extensions in self.destinations.items():
                if extension.lower() in extensions:
                    self.move_file(filename, folder)
                    break

    def organize_by_name_pattern(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(patterns.values())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            for pattern, folder in patterns.items():
                if pattern in filename:
                    self.move_file(filename, folder)
                    break

def admenu():
    while True:
        print("1. Change language")
        print("2. View information")
        print("3. Modify settings")
        print("4. Modify patterns")
        print("5. Return to main menu")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        log_action(f"Admin menu choice: {choice}")

        if choice == '1':
            change_language()
        elif choice == '2':
            view_information()
        elif choice == '3':
            modify_settings()
        elif choice == '4':
            modify_patterns()
        elif choice == '5':
            menu(language)
        elif choice == '6':
            print("Exiting...")
            log_action("Admin exited")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 6.")
            log_action("Invalid admin menu option")

def change_language():
    global language
    print("Available languages: it, en")
    new_language = input("Enter the new language: ").strip().lower()
    if new_language in ["it", "en"]:
        language = new_language
        print(f"Language changed to {language}")
        log_action(f"Language changed to {language}")
    else:
        print("Invalid language.")
        log_action("Attempted to change to invalid language")

def view_information():
    print("Displaying log:")
    show_log()

def modify_settings():
    global destinations
    print("Modifying destination settings:")
    for i, (folder, extensions) in enumerate(destinations.items(), start=1):
        print(f"{i}. {folder} - Extensions: {', '.join(extensions)}")

    print(f"{len(destinations) + 1}. Add a new folder")

    try:
        choice = int(input("Choose a folder to modify or add a new one (number): "))
        if 1 <= choice <= len(destinations):
            folder = list(destinations.keys())[choice - 1]
            print(f"Modifying extensions for {folder}")
            print(f"Current extensions: {', '.join(destinations[folder])}")
            new_extensions = input("Enter new extensions separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            new_extensions = [ext.strip().lower() for ext in new_extensions]
            destinations[folder] = new_extensions
            print(f"Updated extensions for {folder}: {', '.join(destinations[folder])}")
            save_config_to_file()
            log_action(f"Updated extensions for folder '{folder}' to {', '.join(destinations[folder])}")
        elif choice == len(destinations) + 1:
            new_folder = input("Enter the name of the new folder: ").strip()
            new_extensions = input("Enter the extensions for the new folder separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            new_extensions = [ext.strip().lower() for ext in new_extensions]
            destinations[new_folder] = new_extensions
            print(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
            save_config_to_file()
            log_action(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. You must enter a number.")

def modify_patterns():
    global patterns
    print("Modifying name patterns:")
    for i, (pattern, folder) in enumerate(patterns.items(), start=1):
        print(f"{i}. Pattern: '{pattern}' -> Folder: '{folder}'")

    print(f"{len(patterns) + 1}. Add a new pattern")
    print(f"{len(patterns) + 2}. Remove an existing pattern")

    try:
        choice = int(input("Choose an option (number): "))
        if 1 <= choice <= len(patterns):
            pattern = list(patterns.keys())[choice - 1]
            print(f"Modifying folder for pattern '{pattern}'")
            new_folder = input(f"Enter new folder for pattern '{pattern}': ").strip()
            patterns[pattern] = new_folder
            print(f"Updated folder for pattern '{pattern}': {new_folder}")
            save_config_to_file()
            log_action(f"Updated folder for pattern '{pattern}' to {new_folder}")
        elif choice == len(patterns) + 1:
            new_pattern = input("Enter the new pattern: ").strip()
            new_folder = input("Enter the folder for the new pattern: ").strip()
            patterns[new_pattern] = new_folder
            print(f"Added new pattern '{new_pattern}' with folder: '{new_folder}'")
            save_config_to_file()
            log_action(f"Added new pattern '{new_pattern}' with folder: '{new_folder}'")
        elif choice == len(patterns) + 2:
            del_choice = int(input("Enter the number of the pattern to remove: "))
            if 1 <= del_choice <= len(patterns):
                del_pattern = list(patterns.keys())[del_choice - 1]
                del patterns[del_pattern]
                print(f"Removed pattern '{del_pattern}'")
                save_config_to_file()
                log_action(f"Removed pattern '{del_pattern}'")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. You must enter a number.")

def menu(language):
    if language == "it":
        print("Enter commands or type 'help' to see the commands")
    elif language == "en":
        print("Enter commands or type 'help' to see commands")

    command = input("user: ")
    log_action(f"User command: {command}")

    if command == "exit":
        log_action("User exited")
        exit()
    elif command == "organize":
        organizer = FileOrganizer()
        print(f"Source folder: {organizer.source_folder}")
        organizer.organize()
        menu(language)
    elif command == "organize_by_pattern":
        organizer = FileOrganizer()
        print(f"Source folder: {organizer.source_folder}")
        organizer.organize_by_name_pattern()
        menu(language)
    elif command == "admin":
        admin_password = input("Enter the password: ")
        log_action("Admin mode activated")
        if admin_password == "admin":
            print("Admin mode activated")
            admenu()
    elif command == "help":
        if language == "it":
            print("comandi disponibili: organize, organize_by_pattern, exit")
        elif language == "en":
            print("Available commands: organize, organize_by_pattern, exit")
        menu(language)
    else:
        if language == "it":
            print("Unrecognized command")
        elif language == "en":
            print("Unrecognized command")
        log_action("Unrecognized command")
        menu(language)

menu(language)
