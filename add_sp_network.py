import csv

# ── S-box: sustitución fija de 26 letras (A-Z → otra permutación del alfabeto) ──
# Inspirada en el rotor I de Enigma (solo para referencia educativa, determinista)
SBOX = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

# ── Tamaño de bloque y patrón de permutación ────────────────────────────────────
BLOCK_SIZE = 8
# PERM[i] indica la "prioridad" de la posición i al reordenar el bloque
# Resultado: el char con menor PERM[i] pasa al slot 0, el siguiente al slot 1, etc.
PERM = [3, 1, 4, 0, 6, 2, 7, 5]


# ── Paso 1: Sustitución ─────────────────────────────────────────────────────────
def substitute(ch):
    if ch.isalpha():
        base_in  = ord('A') if ch.isupper() else ord('a')
        mapped   = SBOX[ord(ch) - ord('A') if ch.isupper() else ord(ch) - ord('a')]
        # Conservar capitalización original
        return mapped if ch.isupper() else mapped.lower()
    return ch


# ── Paso 2: Permutación de un bloque ───────────────────────────────────────────
def permute_block(chars):
    n = len(chars)
    if n <= 1:
        return list(chars)
    # Genera una permutación válida para cualquier tamaño n usando PERM como clave
    order = sorted(range(n), key=lambda i: PERM[i % len(PERM)])
    return [chars[order[i]] for i in range(n)]


# ── Red de Sustitución-Permutación ─────────────────────────────────────────────
def sp_network(text):
    # 1. Sustitución sobre todos los caracteres alfabéticos
    substituted = [substitute(ch) for ch in text]

    # 2. Permutación: actúa solo sobre las posiciones de letras
    alpha_pos   = [i for i, ch in enumerate(substituted) if ch.isalpha()]
    alpha_chars = [substituted[i] for i in alpha_pos]

    permuted = []
    for start in range(0, len(alpha_chars), BLOCK_SIZE):
        block = alpha_chars[start:start + BLOCK_SIZE]
        permuted.extend(permute_block(block))

    # Reinsertar letras permutadas; los no-alfabéticos quedan en su lugar
    result = list(substituted)
    for idx, pos in enumerate(alpha_pos):
        result[pos] = permuted[idx]

    return ''.join(result)


# ── Main ────────────────────────────────────────────────────────────────────────
path = r'c:\Users\nicoa\Desktop\cripto\romance_dataset.csv'

with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Entradas: {len(rows)}")

if 'sp_network' in rows[0]:
    print("La columna 'sp_network' ya existe. Abortando.")
    exit(1)

if 'vigenere' not in rows[0]:
    print("La columna 'vigenere' no existe. Abortando.")
    exit(1)

for row in rows:
    row['sp_network'] = sp_network(row['vigenere'])

fieldnames = ['id', 'language', 'text', 'text_normalized',
              'caesar', 'vigenere', 'sp_network', 'char_count']

with open(path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Columna 'sp_network' agregada (S-box fija, bloque={BLOCK_SIZE}, PERM={PERM}).")
print("\nEjemplos (flujo completo):")
for row in rows[:3]:
    print(f"  [{row['language']}]")
    print(f"    Normal:     {row['text_normalized']}")
    print(f"    César:      {row['caesar']}")
    print(f"    Vigenere:   {row['vigenere']}")
    print(f"    SP-Network: {row['sp_network']}")
    print()
