import csv
import html
import datetime

def preprocess_berlin_data(input_file="data/berlin_data.csv",
                            output_file="data/berlin_data_clean.csv"):
    """
    Bereinigt die Berlin-Daten:
    - HTML-Zeichen dekodieren
    - Fehlende Werte behandeln
    - Datentypen konvertieren
    - Zeilenumbrüche und überflüssige Leerzeichen entfernen
    - Kategorie-Felder vereinheitlichen
    - Duplikate entfernen
    - Spalte 'region1' entfernen
    - Bereinigte CSV speichern
    """
    # 1. CSV einlesen
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames.copy()
        if 'region1' in fieldnames:
            fieldnames.remove('region1')  # region1 löschen

        berlin_rows = list(reader)

    clean_rows = []
    seen_ids = set()  #Speichert nur eindeutige Werte (keine Duplikate).#Sehr schnell beim Prüfen, ob ein Wert schon vorhanden ist.#mathematic  Sammlung einzigartiger Werte.

    for row in berlin_rows:
        # 2. HTML-Zeichen dekodieren
        for key, value in row.items():
            if value:
                row[key] = html.unescape(value)

        # 3. Fehlende Werte ersetzen
        numeric_fields = ['nebenkosten','grundmiete','gesamt_miete','wohnflaeche','zimmer']
        for field in numeric_fields:
            if row.get(field) in ['NA', '', None]:
                row[field] = 0

        # 4. Datentypen konvertieren
        try:
            row['nebenkosten'] = float(row['nebenkosten'])
            row['grundmiete'] = float(row['grundmiete'])
            row['gesamt_miete'] = float(row['gesamt_miete'])
            row['wohnflaeche'] = float(row['wohnflaeche'])
            row['zimmer'] = int(float(row['zimmer']))
        except:
            pass

        # Datum konvertieren (falls vorhanden, z.B. May19)
        try:
            row['daten_datum'] = datetime.datetime.strptime(row['daten_datum'], "%b%y").strftime("%Y-%m-%d")
        except:
            pass

        # 5. Zeilenumbrüche und überflüssige Leerzeichen entfernen
        text_fields = ['beschreibung','ausstattung','straße','straße_plain']
        for field in text_fields:
            if row.get(field):
                row[field] = " ".join(row[field].split())

        # 6. Kategorie-Felder vereinheitlichen
        category_fields = ['heizungstyp','wohnungstyp','zustand','ausstattungsqualitaet']
        for field in category_fields:
            if row.get(field):
                row[field] = row[field].lower().replace(" ","_")

        # 7. Duplikate entfernen (nach scout_id)
        scout_id = row.get('scout_id')
        if scout_id and scout_id not in seen_ids:
            # region1 entfernen
            if 'region1' in row:
                del row['region1']
            clean_rows.append(row)
            seen_ids.add(scout_id)

    # 8. Bereinigte CSV speichern
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(clean_rows)

    print(f"Bereinigte CSV erstellt (ohne region1): {output_file}")

if __name__ == "__main__":
    preprocess_berlin_data()
