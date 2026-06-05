import csv, unicodedata
from collections import Counter

def normalize(text):
    ligatures = {
        'œ': 'oe', 'Œ': 'OE', 'æ': 'ae', 'Æ': 'AE',
        'ß': 'ss', 'ð': 'd', 'Ð': 'D', 'þ': 'th', 'Þ': 'TH',
        'ŋ': 'n', 'ı': 'i',
    }
    for src, dst in ligatures.items():
        text = text.replace(src, dst)
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')

extra = [
    ("es", "El amor es un fuego que arde sin que nadie lo vea ni lo sienta"),
    ("es", "La grandeza de alma es independiente de la grandeza de sangre"),
    ("es", "No hay cosa más dañina que un amigo que se convierte en enemigo"),
    ("es", "El que no sabe guardar un secreto no merece que se lo cuenten"),
    ("es", "La madre es el primer país que el ser humano habita en su vida"),
    ("es", "No hay mejor maestro en este mundo que el fracaso bien asumido"),
    ("es", "El que calla otorga, dice el refrán que todos conocemos bien"),
    ("es", "La virtud más difícil de practicar es la paciencia con los demás"),
    ("es", "Quien no aprende de la historia está destinado a repetir sus errores"),
    ("es", "El verdadero conocimiento es saber cuánto te falta por aprender"),
    ("es", "La luz al final del túnel es siempre más brillante de lo esperado"),
    ("es", "No hay mayor tesoro en la vida que un buen amigo de verdad"),
    ("es", "El que no arriesga no gana y el que no gana no avanza ni crece"),
    ("es", "La vida nos enseña lo que la escuela nunca pudo ni quiso hacer"),
    ("es", "Quien da sin esperar recompensa recibirá más de lo que imaginó"),
    ("es", "El silencio es la mejor respuesta que puedes dar a la estupidez"),
    ("es", "La confianza se tarda años en construir y segundos en destruir"),
    ("es", "No hay camino que no tenga su propia recompensa al final del día"),
    ("es", "El que vive con miedo muere muchas veces antes de su hora final"),
    ("es", "La sabiduría comienza cuando reconocemos lo que no sabemos aún"),
    ("es", "Quien ayuda a otro sin pedir nada a cambio es verdaderamente libre"),
    ("es", "El libro es el espejo en el que el alma se mira a sí misma"),
    ("es", "La persistencia vence lo que la inteligencia sola no puede lograr"),
    ("en", "The secret of change is to focus all energy not on the old"),
    ("en", "An investment in knowledge pays the best interest of all things"),
    ("en", "Tell me and I forget; teach me and I may remember; involve me"),
    ("en", "In the middle of every difficulty lies opportunity for the brave"),
    ("en", "A journey of a thousand miles begins with a single step forward"),
    ("en", "The only limit to our realization of tomorrow is our doubts today"),
    ("en", "You have brains in your head and feet in your shoes, so go"),
    ("en", "It is never too late to be what you might have been in life"),
    ("en", "The secret of joy in work is contained in one word: excellence"),
    ("en", "Do not wait to strike till the iron is hot but make it hot"),
    ("en", "The only person you are destined to become is the one you decide"),
    ("en", "What lies behind us and before us are small matters indeed"),
    ("en", "Go confidently in the direction of your dreams and live the life"),
    ("en", "You do not find the happy life, you make it with your own hands"),
    ("en", "The good life is one inspired by love and guided by knowledge"),
    ("en", "It is not the mountain we conquer but ourselves in the end"),
    ("en", "Success is not final, failure is not fatal; courage is what counts"),
    ("en", "The world belongs to the energetic and those who never give up"),
    ("en", "Act as if what you do makes a difference, because it actually does"),
    ("en", "In three words I can sum up everything I know about life: it goes on"),
    ("en", "Keep your face always toward the sunshine and shadows will fall"),
    ("en", "With the new day comes new strength and new thoughts for living"),
    ("en", "Do what you can with all you have wherever you happen to be"),
]

path = r'C:\Users\nicoa\romance_dataset.csv'
with open(path, encoding='utf-8') as f:
    existing = list(csv.DictReader(f))

existing_texts = {r['text'] for r in existing}
max_id = max(int(r['id']) for r in existing)
needed = 1000 - len(existing)
print(f"Entradas actuales: {len(existing)}, faltan: {needed}")

seen = set(existing_texts)
filtered = []
for lang, text in extra:
    t = text.strip()
    if 50 <= len(t) <= 100 and t not in seen:
        seen.add(t)
        filtered.append((lang, t))

final_new = filtered[:needed]
print(f"Frases extra validas: {len(filtered)}, agregando: {len(final_new)}")

all_rows = existing.copy()
for i, (lang, text) in enumerate(final_new, max_id + 1):
    all_rows.append({
        'id': i,
        'language': lang,
        'text': text,
        'text_normalized': normalize(text),
        'char_count': len(text),
    })

with open(path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=['id', 'language', 'text', 'text_normalized', 'char_count'],
        quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    writer.writerows(all_rows)

with open(path, encoding='utf-8') as f:
    final = list(csv.DictReader(f))

lang_counts = Counter(r['language'] for r in final)
lengths = [int(r['char_count']) for r in final]
print(f"\nTotal entradas: {len(final)}")
print(f"Chars: min={min(lengths)}, max={max(lengths)}, avg={sum(lengths)/len(lengths):.1f}")
print("\nDistribucion por idioma:")
for lang, count in sorted(lang_counts.items()):
    print(f"  {lang}: {count}")
