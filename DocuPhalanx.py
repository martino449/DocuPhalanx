import os
import shutil
import json
from datetime import datetime
from config import destinations, lingua as linguaggio

CONFIG_FILE = 'config.py'

def log_action(action):
    log_folder = os.path.join(os.getcwd(), 'program')
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
    log_file_path = os.path.join(os.getcwd(), 'program', 'log.json')

    if not os.path.exists(log_file_path):
        print("Nessun log trovato.")
        return

    with open(log_file_path, 'r') as file:
        data = json.load(file)

    if not data:
        print("Il log è vuoto.")
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
        if source_folder is None:
            self.source_folder = self.get_source_folder()
        else:
            self.source_folder = source_folder
        self.destinations = destinations

    def get_source_folder(self):
        current_dir = os.getcwd()
        return current_dir

    def create_destination_folders(self):
        for folder in self.destinations:
            folder_path = os.path.join(self.source_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_file(self, filename):
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
        if not os.path.exists(self.source_folder):
            print(f"La cartella {self.source_folder} non esiste.")
            return
        self.create_destination_folders()
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            self.move_file(filename)

def admenu():
    while True:
        print("1. Cambia lingua")
        print("2. Visualizza informazioni")
        print("3. Modifica impostazioni")
        print("4. Visualizza statistiche")
        print("5. Esci")

        choice = input("Scegli un'opzione (1-5): ").strip()
        log_action(f"Admin menu choice: {choice}")

        if choice == '1':
            cambia_lingua()
        elif choice == '2':
            visualizza_informazioni()
        elif choice == '3':
            modifica_impostazioni()
        elif choice == '4':
            visualizza_statistiche()
        elif choice == '5':
            print("Uscita...")
            log_action("Admin exited")
            break
        else:
            print("Opzione non valida. Per favore, scegli un'opzione tra 1 e 5.")
            log_action("Invalid admin menu option")

def cambia_lingua():
    global linguaggio
    print("Lingue disponibili: it, en")
    nuova_lingua = input("Inserisci la nuova lingua: ").strip().lower()
    if nuova_lingua in ["it", "en"]:
        linguaggio = nuova_lingua
        print(f"Lingua cambiata a {linguaggio}")
        log_action(f"Language changed to {linguaggio}")
    else:
        print("Lingua non valida.")
        log_action("Attempted to change to invalid language")

def visualizza_informazioni():
    print("Visualizzazione del log:")
    show_log()

def modifica_impostazioni():
    global destinations
    print("Modifica delle impostazioni delle destinazioni:")
    for i, (folder, extensions) in enumerate(destinations.items(), start=1):
        print(f"{i}. {folder} - Estensioni: {', '.join(extensions)}")

    try:
        scelta = int(input("Scegli una cartella da modificare (numero): "))
        if 1 <= scelta <= len(destinations):
            folder = list(destinations.keys())[scelta - 1]
            print(f"Modifica estensioni per {folder}")
            print(f"Estensioni attuali: {', '.join(destinations[folder])}")
            nuove_estensioni = input("Inserisci le nuove estensioni separate da virgola (es. .pdf, .docx): ").strip().split(',')
            nuove_estensioni = [ext.strip().lower() for ext in nuove_estensioni]
            destinations[folder] = nuove_estensioni
            print(f"Estensioni aggiornate per {folder}: {', '.join(destinations[folder])}")
            save_destinations_to_config()
            log_action(f"Updated extensions for folder '{folder}' to {', '.join(destinations[folder])}")
        else:
            print("Scelta non valida.")
    except ValueError:
        print("Inserimento non valido. Devi inserire un numero.")

def visualizza_statistiche():
    print("Statistiche dei file per tipo di destinazione:")
    for folder in destinations:
        folder_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(folder_path):
            num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
            print(f"{folder}: {num_files} file")
        else:
            print(f"{folder}: Cartella non trovata")
    log_action("Displayed file statistics")

def menu(lingua):
    if lingua == "it":
        print("Inserire comandi o scrivere 'help' per visualizzare i comandi")
    elif lingua == "en":
        print("Enter commands or type 'help' to see commands")

    comando = input("user: ")
    log_action(f"User command: {comando}")

    if comando == "exit":
        log_action("User exited")
        exit()
    elif comando == "organizza":
        organizer = FileOrganizer()
        print(f"Cartella sorgente: {organizer.source_folder}")
        organizer.organize()
        menu(linguaggio)
    elif comando == "admin":
        adpass = input("Inserire la password: ")
        log_action("Admin mode activated")
        if adpass == "admin":
            print("Attivata modalità amministratore")
            admenu()
    elif comando == "help":
        if lingua == "it":
            print("Comandi disponibili: organizza, exit, admin")
        elif lingua == "en":
            print("Available commands: organize, exit, admin")
        menu(linguaggio)
    else:
        if lingua == "it":
            print("Comando non riconosciuto")
        elif lingua == "en":
            print("Unrecognized command")
        log_action("Unrecognized command")
        menu(linguaggio)

menu(linguaggio)
