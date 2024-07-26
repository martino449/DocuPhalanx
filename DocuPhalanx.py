import os
import shutil
import json
from datetime import datetime
language = "it"
from config import destinations as destinations

CONFIG_FILE = 'config.py'

def log_action(action):
    # Create a log folder if it doesn't exist
    log_folder = os.path.join(os.getcwd(), 'DPLOG')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the path for the log file
    log_file_path = os.path.join(log_folder, 'log.json')

    # Create a log entry with the current timestamp and action
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action
    }

    # Read existing log data if the file exists
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Append the new log entry
    data.append(log_entry)

    # Write the updated log data to the file
    with open(log_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def show_log():
    # Define the path for the log file
    log_file_path = os.path.join(os.getcwd(), 'DPLOG', 'log.json')

    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print("No log found.")
        return

    # Read and display the log data
    with open(log_file_path, 'r') as file:
        data = json.load(file)

    if not data:
        print("The log is empty.")
        return

    for entry in data:
        print(f"{entry['timestamp']}: {entry['action']}")

def save_destinations_to_config():
    # Write the updated destinations to the config file
    config_content = f"destinations = {json.dumps(destinations, indent=4)}\n"
    with open(CONFIG_FILE, 'w') as file:
        file.write(config_content)

class FileOrganizer:
    def __init__(self, source_folder=None):
        # Initialize the source folder, either from the parameter or by default
        if source_folder is None:
            self.source_folder = self.get_source_folder()
        else:
            self.source_folder = source_folder

        self.destinations = destinations

    def get_source_folder(self):
        # Get the current working directory as the source folder
        current_dir = os.getcwd()
        return current_dir

    def create_destination_folders(self):
        # Create destination folders if they don't exist
        for folder in self.destinations:
            folder_path = os.path.join(self.source_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_file(self, filename):
        # Move a file to the appropriate destination folder based on its extension
        file_path = os.path.join(self.source_folder, filename)
        _, extension = os.path.splitext(filename)
        for folder, extensions in self.destinations.items():
            if extension.lower() in extensions:
                destination_path = os.path.join(self.source_folder, folder, filename)
                shutil.move(file_path, destination_path)
                print(f"Moved: {filename} -> {folder}")
                log_action(f"Moved file: {filename} to {folder}")
                break

    def organize(self):
        # Organize files in the source folder
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders()
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            self.move_file(filename)

def admenu():
    # Display the admin menu and handle user choices
    while True:
        print("1. Change language")
        print("2. View information")
        print("3. Modify settings")
        print("4. Return to main menu")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()
        log_action(f"Admin menu choice: {choice}")

        if choice == '1':
            change_language()
        elif choice == '2':
            view_information()
        elif choice == '3':
            modify_settings()
        elif choice == '4':
            menu(language)
        elif choice == '5':
            print("Exiting...")
            log_action("Admin exited")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 5.")
            log_action("Invalid admin menu option")

def change_language():
    # Change the language setting
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
    # Display the log information
    print("Displaying log:")
    show_log()

def modify_settings():
    # Modify the destination folder settings
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
            save_destinations_to_config()
            log_action(f"Updated extensions for folder '{folder}' to {', '.join(destinations[folder])}")
        elif choice == len(destinations) + 1:
            new_folder = input("Enter the name of the new folder: ").strip()
            new_extensions = input("Enter the extensions for the new folder separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            new_extensions = [ext.strip().lower() for ext in new_extensions]
            destinations[new_folder] = new_extensions
            print(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
            save_destinations_to_config()
            log_action(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. You must enter a number.")

def menu(language):
    # Display the main menu and handle user commands
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
    elif command == "admin":
        admin_password = input("Enter the password: ")
        log_action("Admin mode activated")
        if admin_password == "admin":
            print("Admin mode activated")
            admenu()
    elif command == "help":
        if language == "it":
            print("comandi disponibili: organize, exit")
        elif language == "en":
            print("Available commands: organize, exit")
        menu(language)
    else:
        if language == "it":
            print("Unrecognized command")
        elif language == "en":
            print("Unrecognized command")
        log_action("Unrecognized command")
        menu(language)

# Start the program with the current language setting
menu(language)

