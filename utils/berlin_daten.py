import csv

input_file = "data/immo_data.csv"      
output_file = "data/berlin_data.csv"    
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, quotechar='"', doublequote=True)
    fieldnames = reader.fieldnames
    
    berlin_rows = [
        row for row in reader
        if ('berlin' in (row.get('region1') or '').lower() or
            'berlin' in (row.get('region2') or '').lower() or
            'berlin' in (row.get('region3') or '').lower())
    ]

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerows(berlin_rows)

print(f"CSV für Berlin erstellt: {output_file}")
