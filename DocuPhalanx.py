import os
import shutil
import json
from datetime import datetime
from config import destinations, patterns

CONFIG_FILE = 'config.py'

IGNORE_EXTENSIONS = {
    '.py', '.toml', '.lock', '.cache', '.replit', '.git', '.gitignore', 
    '.gitattributes', '.gitmodules', '.DS_Store'
}

language = "en"

def log_action(action):
    log_folder = os.path.join(os.getcwd(), 'DPLOG')
    os.makedirs(log_folder, exist_ok=True)

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
        self.source_folder = source_folder or os.getcwd()
        self.destinations = destinations

    def create_destination_folders(self, folders):
        for folder in folders:
            folder_path = os.path.join(self.source_folder, folder)
            os.makedirs(folder_path, exist_ok=True)

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
            if os.path.isdir(file_path) or os.path.splitext(filename)[1].lower() in IGNORE_EXTENSIONS:
                continue

            for folder, extensions in self.destinations.items():
                if os.path.splitext(filename)[1].lower() in extensions:
                    self.move_file(filename, folder)
                    break

    def organize_by_name_pattern(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return

        self.create_destination_folders(patterns.values())

        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path) or any(filename.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue

            for pattern, folder in patterns.items():
                if pattern in filename:
                    self.move_file(filename, folder)
                    break

    def organize_by_size(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return

        size_categories = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gigantic']
        self.create_destination_folders(size_categories)

        size_limits = [
            (1024, 'Tiny'), 
            (1048576, 'Small'), 
            (10485760, 'Medium'), 
            (104857600, 'Large'), 
            (1073741824, 'Huge')
        ]

        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path) or os.path.splitext(filename)[1].lower() in IGNORE_EXTENSIONS:
                continue

            file_size = os.path.getsize(file_path)
            category = next((cat for size, cat in reversed(size_limits) if file_size < size), 'Gigantic')
            self.move_file(filename, category)

def unified_menu(language="en"):
    greetings = {
        "it": "Inserisci comandi o digita 'help' per vedere i comandi",
        "en": "Enter commands or type 'help' to see commands"
    }
    print(greetings.get(language, greetings["en"]))

    menu_options = {
        "1": lambda: execute_organizer_command('organize'),
        "2": lambda: execute_organizer_command('organize_by_name_pattern'),
        "3": lambda: execute_organizer_command('organize_by_size'),
        "4": change_language,
        "5": view_information,
        "6": modify_settings,
        "7": modify_patterns,
        "8": exit_program
    }

    while True:
        print("\nMain Menu:")
        print("1. Organize files")
        print("2. Organize files by name pattern")
        print("3. Organize files by size")
        print("4. Change language")
        print("5. View log")
        print("6. Modify destination settings")
        print("7. Modify name patterns")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()
        log_action(f"Menu choice: {choice}")

        if choice in menu_options:
            menu_options[choice]()
        else:
            print("Invalid option. Please choose a number between 1 and 8.")
            log_action("Invalid menu option")

def change_language():
    global language
    available_languages = {"it", "en"}
    print("Available languages: it, en")
    new_language = input("Enter the new language: ").strip().lower()

    if new_language in available_languages:
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
            destinations[folder] = [ext.strip().lower() for ext in new_extensions]
            print(f"Updated extensions for {folder}: {', '.join(destinations[folder])}")
            save_config_to_file()
            log_action(f"Updated extensions for folder '{folder}' to {', '.join(destinations[folder])}")
        elif choice == len(destinations) + 1:
            new_folder = input("Enter the name of the new folder: ").strip()
            new_extensions = input("Enter the extensions for the new folder separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            destinations[new_folder] = [ext.strip().lower() for ext in new_extensions]
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

def execute_organizer_command(command):
    organizer = FileOrganizer()
    print(f"Source folder: {organizer.source_folder}")
    getattr(organizer, command)()

def exit_program():
    print("Exiting...")
    log_action("User exited")
    exit()

unified_menu(language)

#Fine del codice
# ---------------------------------------------
# Copyright (c) 2024 Mario Pisano
#
# Questo programma è distribuito sotto la licenza EUPL, Versione 1.2 o – non appena 
# saranno approvate dalla Commissione Europea – versioni successive della EUPL 
# (la "Licenza");
# Puoi usare, modificare e/o ridistribuire il programma sotto i termini della 
# Licenza. 
# 
# Puoi trovare una copia della Licenza all'indirizzo:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
