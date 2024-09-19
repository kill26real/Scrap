import re
import os
import csv
from tqdm import tqdm

# Pfad zum Marken CSV
marken_csv = 'words2.csv'

# Pfad zum Textordner
text_folder = '2024-07_deep'

def search_for_brands(text, brands):
    found_brands = []
    for brand in brands:
        try:
            if re.search(r'\b' + re.escape(brand.lower()) + r'\b', text.lower()):
                found_brands.append(brand)
        except Exception as e:
            print(f"Fehler bei der Suche nach Marke '{brand}': {e}")
    return found_brands

def load_brands_from_csv(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        return [row['Brandname'] for row in reader]

def main():
    tqdm.write("Laden der Marken aus der CSV-Datei...")
    marken = load_brands_from_csv(marken_csv)

    tqdm.write("Laden der zuletzt verarbeiteten ID...")
    try:
        with open('last_id.txt', 'r') as f:
            last_id = int(f.read())
    except FileNotFoundError:
        last_id = None

    tqdm.write("Öffnen der Ausgabe-CSV-Datei...")
    with open('output.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        tqdm.write("Beginn der Verarbeitung der Textdateien...")
        for folder in tqdm(sorted(os.listdir(text_folder), key=int)):
            if last_id is not None and int(folder) <= last_id:
                continue

            for filename in os.listdir(os.path.join(text_folder, folder)):
                if not filename.endswith('.txt'):
                    continue

                tqdm.write(f"Verarbeiten der Datei {filename} im Ordner {folder}...")
                with open(os.path.join(text_folder, folder, filename), 'r', encoding='utf-8') as f:
                    text = f.read()

                found_brands = search_for_brands(text, marken)

                tqdm.write(f"Gefundene Marken in {filename}: {found_brands}")
                writer.writerow([folder] + found_brands)

                # Leert den Puffer und schreibt alle gepufferten Daten sofort auf die Festplatte.
                csvfile.flush()

            with open('last_id.txt', 'w') as f:
                f.write(folder)

    tqdm.write("Fertig mit der Verarbeitung der Textdateien.")

if __name__ == "__main__":
    main()