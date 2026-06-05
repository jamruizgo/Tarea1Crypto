import csv

SHIFT = 3

def caesar(text, shift=SHIFT):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

path = r'C:\Users\nicoa\romance_dataset.csv'

with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Entradas: {len(rows)}")

# Verificar que no exista ya la columna
if 'caesar' in rows[0]:
    print("La columna 'caesar' ya existe. Abortando.")
    exit(1)

for row in rows:
    row['caesar'] = caesar(row['text_normalized'])

fieldnames = ['id', 'language', 'text', 'text_normalized', 'caesar', 'char_count']

with open(path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Columna 'caesar' agregada (shift={SHIFT}).")
print("\nEjemplos:")
for row in rows[:5]:
    print(f"  [{row['language']}] {row['text_normalized']}")
    print(f"       -> {row['caesar']}")
    print()
