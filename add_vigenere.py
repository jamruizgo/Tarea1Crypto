import csv

KEY = "AMOR"  # Clave Vigenere (solo letras, se usa en mayusculas internamente)

def vigenere(text, key):
    key = key.upper()
    result = []
    key_index = 0  # avanza solo con letras
    for ch in text:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return ''.join(result)

path = r'c:\Users\nicoa\Desktop\cripto\romance_dataset.csv'

with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Entradas: {len(rows)}")

if 'vigenere' in rows[0]:
    print("La columna 'vigenere' ya existe. Abortando.")
    exit(1)

if 'caesar' not in rows[0]:
    print("La columna 'caesar' no existe. Abortando.")
    exit(1)

for row in rows:
    row['vigenere'] = vigenere(row['caesar'], KEY)

fieldnames = ['id', 'language', 'text', 'text_normalized', 'caesar', 'vigenere', 'char_count']

with open(path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Columna 'vigenere' agregada (key='{KEY}').")
print("\nEjemplos:")
for row in rows[:5]:
    print(f"  [{row['language']}] Caesar:   {row['caesar']}")
    print(f"             Vigenere: {row['vigenere']}")
    print()
