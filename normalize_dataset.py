import csv, unicodedata

def normalize(text):
    # Expandir ligaduras antes de descomponer
    ligatures = {
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
        'ß': 'ss',
        'ð': 'd',  'Ð': 'D',
        'þ': 'th', 'Þ': 'TH',
        'ŋ': 'n',  'ı': 'i',
        'ĸ': 'k',  'ŀ': 'l', 'Ŀ': 'L',
    }
    for src, dst in ligatures.items():
        text = text.replace(src, dst)
    # Descomponer y eliminar marcas diacríticas (categoría Mn)
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')

path = r'C:\Users\nicoa\romance_dataset.csv'

with open(path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

with open(path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=['id', 'language', 'text', 'text_normalized', 'char_count'],
        quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    for row in rows:
        row['text_normalized'] = normalize(row['text'])
        writer.writerow(row)

# Verificación
with open(path, encoding='utf-8') as f:
    sample = list(csv.DictReader(f))

print(f'OK - {len(sample)} filas')
print(f'Columnas: {list(sample[0].keys())}')
print()
print('Ejemplos de normalizacion:')
shown = 0
for r in sample:
    if r['text'] != r['text_normalized']:
        lang = r['language']
        print(f'  [{lang}] {r["text"]}')
        print(f'       -> {r["text_normalized"]}')
        shown += 1
        if shown == 6:
            break
