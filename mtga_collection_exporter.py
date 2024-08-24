import json
import csv
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def select_log_file():
    global log_file_path
    log_file_path = filedialog.askopenfilename(title="Select the UTC_Log file", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
    log_file_label.config(text=f"Selected Log File: {log_file_path}")

def select_allprintings_file():
    global allprintings_file_path
    allprintings_file_path = filedialog.askopenfilename(title="Select the AllPrintings.json file", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    allprintings_file_label.config(text=f"Selected AllPrintings File: {allprintings_file_path}")

def extract_card_ids(log_file_path):
    card_ids = {}
    deck_patterns = [
        r'CourseDeck',
        r'MainDeck',
        r'Deck_UpsertDeckV2',
        r'Event_SetDeckV2',
        r'InventoryInfo'
    ]
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if any(re.search(pattern, line) for pattern in deck_patterns):
                try:
                    json_start = line.find('{')
                    if json_start != -1:
                        json_data = json.loads(line[json_start:])
                        
                        def extract_card_ids_recursive(data):
                            if isinstance(data, dict):
                                if 'MainDeck' in data:
                                    for card in data['MainDeck']:
                                        card_id = str(card['cardId'])
                                        quantity = card['quantity']
                                        card_ids[card_id] = card_ids.get(card_id, 0) + quantity
                                elif 'InventoryInfo' in data:
                                    pass
                                else:
                                    for value in data.values():
                                        if isinstance(value, (dict, list)):
                                            extract_card_ids_recursive(value)
                            elif isinstance(data, list):
                                for item in data:
                                    extract_card_ids_recursive(item)
                        
                        extract_card_ids_recursive(json_data)
                        
                except json.JSONDecodeError:
                    print(f"Errore nel parsing JSON della riga: {line[:100]}...")
                except Exception as e:
                    print(f"Errore nel processare la riga: {line[:100]}...")
                    print(f"Eccezione: {e}")
    
    return card_ids

def load_card_names(allprintings_file_path):
    card_names = {}
    arena_ids_found = set()
    with open(allprintings_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for set_code, set_data in data['data'].items():
            for card in set_data['cards']:
                if 'identifiers' in card and 'mtgArenaId' in card['identifiers']:
                    arena_id = card['identifiers']['mtgArenaId']
                    card_names[arena_id] = card['name']
                    arena_ids_found.add(arena_id)
    
    print(f"Trovati {len(arena_ids_found)} ID Arena unici in AllPrintings.json")
    print(f"Primi 10 ID Arena trovati: {list(arena_ids_found)[:10]}")
    return card_names

def convert_ids_to_names(card_ids, card_names):
    converted = []
    for card_id, quantity in card_ids.items():
        name = card_names.get(card_id, 'Unknown')
        if name == 'Unknown':
            name = card_names.get(str(card_id), 'Unknown')  # Prova anche con l'ID come stringa
        converted.append((card_id, name, quantity))
    
    unknown_count = sum(1 for _, name, _ in converted if name == 'Unknown')
    print(f"Carte non trovate: {unknown_count} su {len(converted)}")
    return converted

def save_to_csv(card_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['cardId', 'cardName', 'quantity'])  # Intestazione del CSV
        for card_id, card_name, quantity in card_data:
            csvwriter.writerow([card_id, card_name, quantity])

def run_extraction():
    if log_file_path:
        card_ids = extract_card_ids(log_file_path)
        output_file = f"deck_card_ids_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_to_csv([(id, '', quantity) for id, quantity in card_ids.items()], output_file)
        total_cards = sum(card_ids.values())
        result_label.config(text=f"{len(card_ids)} unique Card IDs from decks (total {total_cards} cards) exported to {output_file}")
    else:
        result_label.config(text="Select a log file before running the extraction.")

def run_conversion():
    if log_file_path and allprintings_file_path:
        card_ids = extract_card_ids(log_file_path)
        card_names = load_card_names(allprintings_file_path)
        card_data = convert_ids_to_names(card_ids, card_names)
        output_file = f"deck_card_names_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_to_csv(card_data, output_file)
        total_cards = sum(card_ids.values())
        unknown_count = sum(1 for _, name, _ in card_data if name == 'Unknown')
        result_label.config(text=f"{len(card_data)} Card IDs processed. {unknown_count} unknown. Total {total_cards} cards. Exported to {output_file}")
    else:
        result_label.config(text="Select both log file and AllPrintings file before converting.")

# Creazione della finestra principale
root = tk.Tk()
root.title("MTGA Deck Card ID Exporter and Converter")

log_file_path = ""
allprintings_file_path = ""

log_file_button = tk.Button(root, text="Select UTC_Log File", command=select_log_file)
log_file_button.pack(pady=10)

log_file_label = tk.Label(root, text="No Log File Selected")
log_file_label.pack(pady=5)

allprintings_file_button = tk.Button(root, text="Select AllPrintings.json", command=select_allprintings_file)
allprintings_file_button.pack(pady=10)

allprintings_file_label = tk.Label(root, text="No AllPrintings File Selected")
allprintings_file_label.pack(pady=5)

extract_button = tk.Button(root, text="Extract Card IDs", command=run_extraction)
extract_button.pack(pady=10)

convert_button = tk.Button(root, text="Convert to Card Names", command=run_conversion)
convert_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
