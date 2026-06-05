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
    ("fr", "On n'apprend pas au vieux singe à faire des grimaces"),
    ("fr", "Autant en emporte le vent et l'oubli efface tout le reste"),
    ("fr", "Un tiens vaut mieux que deux tu l'auras selon la sagesse"),
    ("fr", "Il faut que jeunesse se passe et que vieillesse se repose"),
    ("fr", "Qui vivra verra car le temps révèle ce que l'on cache"),
    ("fr", "C'est en forgeant que l'on devient forgeron et non autrement"),
    ("fr", "Beaucoup de bruit pour peu de chose comme dit Shakespeare"),
    ("fr", "Qui paye ses dettes s'enrichit et dort mieux la nuit"),
    ("fr", "On ne peut pas être au four et au moulin en même temps"),
    ("fr", "Il faut que tout change pour que tout reste comme avant"),
    ("fr", "La fortune ne sourit qu'une fois mais la persévérance revient"),
    ("fr", "Tout est bien qui finit bien dit le vieux proverbe sage"),
    ("fr", "Qui sème le vent récolte toujours la tempête un jour"),
    ("fr", "On ne juge pas un livre à sa couverture mais à son contenu"),
    ("fr", "Les grandes douleurs sont muettes mais les petites crient fort"),
    ("fr", "Qui cherche trouve et qui frappe à la porte elle s'ouvre"),
    ("fr", "L'amour est aveugle mais le mariage lui rend la vue"),
    ("fr", "Tout finit par se savoir car la vérité ne reste pas cachée"),
    ("fr", "La vie est belle quand on la vit avec simplicité et joie"),
    ("fr", "Il ne faut pas se fier aux apparences car elles trompent"),
    ("it", "La vita premia i coraggiosi che non si arrendono mai"),
    ("it", "Non esistono scorciatoie per i luoghi che valgono la pena"),
    ("it", "Chi non ha mai fallito non ha mai provato qualcosa di grande"),
    ("it", "La sconfitta è solo una pausa nel cammino verso il successo"),
    ("it", "Non è importante quante volte cadi ma quante volte ti rialzi"),
    ("it", "Chi impara dai propri errori è più saggio di chi non erra"),
    ("it", "La mente che si apre a un'idea nuova non torna mai indietro"),
    ("it", "Non si può insegnare tutto ma si può imparare ovunque"),
    ("it", "La vera ricchezza non sta in quello che hai ma in quello sei"),
    ("it", "Chi vive nel presente non ha rimpianti per il passato"),
    ("pt", "A vida ensina mais do que qualquer escola do mundo inteiro"),
    ("pt", "Não há fracasso definitivo enquanto houver vontade de tentar"),
    ("pt", "Quem não falha nunca tentou nada que valha a pena de verdade"),
    ("pt", "A derrota é apenas uma pausa no caminho para o sucesso"),
    ("pt", "Não importa quantas vezes caíste mas quantas te levantaste"),
    ("pt", "Quem aprende com os próprios erros é mais sábio que os outros"),
    ("pt", "A mente que se abre a uma nova ideia nunca mais volta atrás"),
    ("pt", "Não se pode ensinar tudo mas pode-se aprender em todo o lado"),
    ("pt", "A verdadeira riqueza não está no que tens mas no que és"),
    ("pt", "Quem vive no presente não tem saudade nem medo do futuro"),
    ("es", "La vida enseña más que cualquier escuela del mundo entero"),
    ("es", "No hay fracaso definitivo mientras haya voluntad de intentar"),
    ("es", "Quien nunca falla nunca intentó nada que merezca la pena"),
    ("es", "La derrota es solo una pausa en el camino hacia el éxito"),
    ("es", "No importa cuántas veces caíste sino cuántas te levantaste"),
    ("es", "Quien aprende de sus propios errores es más sabio que otros"),
    ("es", "La mente que se abre a una idea nueva nunca vuelve atrás"),
    ("es", "No se puede enseñar todo pero se puede aprender en todos lados"),
    ("es", "La verdadera riqueza no está en lo que tienes sino en lo que eres"),
    ("es", "Quien vive en el presente no tiene añoranzas ni miedos futuros"),
    ("en", "Life rewards those who work hard and never give up trying"),
    ("en", "There is no shortcut to any place worth going in this life"),
    ("en", "He who has never failed has never tried anything truly great"),
    ("en", "Defeat is only a pause in the journey toward eventual success"),
    ("en", "It does not matter how many times you fall only how you rise"),
    ("en", "He who learns from his mistakes is wiser than he who does not"),
    ("en", "A mind stretched by a new idea can never go back to old size"),
    ("en", "You cannot teach everything but you can learn something always"),
    ("en", "True wealth lies not in what you have but in what you are"),
    ("en", "Who lives in the present has no regrets and no fears ahead"),
    ("en", "The secret ingredient to every great life is showing up daily"),
    ("en", "Do not let what you cannot do interfere with what you can"),
    ("en", "Every accomplishment starts with the decision to try it once"),
    ("en", "Keep your face toward the sunshine and shadows fall behind"),
    ("en", "The will to win the desire to succeed can do anything"),
    ("en", "If your dreams do not scare you they are not big enough yet"),
    ("en", "What you get by achieving your goals is not as important as"),
    ("en", "Believe you deserve it and the universe will serve it to you"),
    ("en", "Push yourself because no one else is going to do it for you"),
    ("en", "Sometimes later becomes never so do it now without waiting"),
    ("en", "Great things never come from comfort zones of ordinary life"),
    ("en", "Dream it wish it do it and watch what happens to your life"),
    ("en", "Stay focused and never give up no matter how hard it gets"),
    ("en", "The key to success is to start before you are ready for it"),
    ("en", "Make today so awesome that yesterday gets jealous of you"),
    ("en", "Work hard in silence let success be your noise to the world"),
    ("en", "Do something today that your future self will be thankful for"),
    ("en", "Little things make big days when you pay close attention"),
    ("en", "It is going to be hard but hard is not the same as impossible"),
    ("en", "The most difficult thing is the decision to act the rest easy"),
    ("ro", "Viața răsplătește pe cei ce muncesc din greu și perseverează"),
    ("ro", "Nu există scurtătură spre locurile care merită cu adevărat"),
    ("ro", "Cel ce n-a eșuat niciodată n-a încercat nimic cu adevărat"),
    ("ro", "Înfrângerea este o pauză pe drumul spre succes și victorie"),
    ("ro", "Nu contează de câte ori ai căzut ci de câte ori te-ai ridicat"),
    ("ro", "Cel ce învață din greșelile proprii este mai înțelept ca toți"),
    ("ro", "O minte deschisă la idei noi nu mai revine la starea veche"),
    ("ro", "Nu poți învăța totul dar poți învăța ceva de oriunde"),
    ("ro", "Adevărata bogăție nu stă în ce ai ci în ceea ce ești"),
    ("ro", "Cel ce trăiește în prezent nu are regrete nici temeri"),
    ("ca", "La vida premia els qui treballen fort i mai no es rendeixen"),
    ("ca", "No hi ha drecera cap als llocs que de veritat valen la pena"),
    ("ca", "Qui no ha fracassat mai no ha intentat res gran de veritat"),
    ("ca", "La derrota és només una pausa en el camí cap a l'èxit"),
    ("ca", "No importa quantes vegades has caigut sinó quantes t'has aixecat"),
    ("ca", "Qui aprèn dels propis errors és més savi que tots els altres"),
    ("ca", "Una ment oberta a idees noves mai pot tornar enrere"),
    ("ca", "No es pot ensenyar tot però es pot aprendre arreu"),
    ("ca", "La riquesa vera no és en el que tens sinó en el que ets"),
    ("ca", "Qui viu en el present no té enyorança ni por del demà"),
    ("gl", "A vida premia os que traballan duro e nunca se renden"),
    ("gl", "Non hai atallos cara aos lugares que de verdade valen a pena"),
    ("gl", "Quen nunca fracasou nunca intentou nada grande de verdade"),
    ("gl", "A derrota é só unha pausa no camiño cara ao éxito final"),
    ("gl", "Non importa cantas veces caíches senón cantas te levantaches"),
    ("oc", "La vida recompensa los que trabalhan fòrt e que persèveran"),
    ("oc", "Non i a drecièra cap als luòcs que vertadièrament valon"),
    ("oc", "Qui a jamai fracassat jamai a provat quicòm grand de ver"),
    ("oc", "La desfacha es solament una pausa sul camin cap al triomf"),
    ("oc", "Non importa quanàtas còps es tombat mas quanàtas s'es levat"),
    ("la", "Qui laborat orat et qui orat laborat pro gloria Dei"),
    ("la", "Vita sine litteris mors est et sepultura vivi hominis"),
    ("la", "Bene qui latuit bene vixit et sapienter se abscondere"),
    ("la", "Omnia aliena sunt tempus tantum nostrum est et pretiosum"),
    ("la", "Inimica est magnorum hominum cogitationibus solitudo"),
]

path = r'C:\Users\nicoa\romance_dataset.csv'
with open(path, encoding='utf-8') as f:
    existing = list(csv.DictReader(f))

existing_texts = {r['text'] for r in existing}
max_id = max(int(r['id']) for r in existing)
needed = 2000 - len(existing)
print(f"Entradas actuales: {len(existing)}, faltan: {needed}")

seen = set(existing_texts)
filtered = []
for lang, text in extra:
    t = text.strip()
    if 50 <= len(t) <= 100 and t not in seen:
        seen.add(t)
        filtered.append((lang, t))

final_new = filtered[:needed]
print(f"Frases válidas disponibles: {len(filtered)}, agregando: {len(final_new)}")

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
