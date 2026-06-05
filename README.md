# Dataset de Cifrado en Lenguas Romances

Pipeline de cifrado progresivo aplicado a 2000 textos en lenguas romances.
Cada texto pasa por tres capas de cifrado encadenadas, y el resultado de cada etapa
queda almacenado como una columna independiente en `romance_dataset.csv`.

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `generate_romance_dataset.py` | Genera el dataset inicial con textos originales |
| `normalize_dataset.py` | Normaliza el texto (elimina acentos y ligaduras) |
| `add_caesar.py` | Aplica cifrado César y agrega la columna `caesar` |
| `add_vigenere.py` | Aplica cifrado Vigenère sobre César y agrega `vigenere` |
| `add_sp_network.py` | Aplica red de Sustitución-Permutación sobre Vigenère y agrega `sp_network` |
| `romance_dataset.csv` | Dataset final con todas las columnas |

---

## Estructura del dataset (`romance_dataset.csv`)

| Columna | Descripción |
|---|---|
| `id` | Identificador numérico único |
| `language` | Código del idioma (`fr`, `pt`, `it`, `ro`, `ca`, `la`, `gl`, `oc`) |
| `text` | Texto original con acentos y caracteres especiales |
| `text_normalized` | Texto sin acentos ni ligaduras (base de todos los cifrados) |
| `caesar` | Texto cifrado con César (shift = 3) sobre `text_normalized` |
| `vigenere` | Texto cifrado con Vigenère (clave `AMOR`) sobre `caesar` |
| `sp_network` | Texto cifrado con Red S-P (S-box + permutación) sobre `vigenere` |
| `char_count` | Longitud del texto normalizado |

---

## Flujo de cifrado

```
text_normalized  →  [César]  →  caesar  →  [Vigenère]  →  vigenere  →  [SP-Network]  →  sp_network
```

Ejemplo con la primera fila del dataset:

| Etapa | Texto |
|---|---|
| Normal | `L'homme est ne libre, et partout il est dans les fers` |
| César | `O'krpph hvw qh oleuh, hw sduwrxw lo hvw gdqv ohv ihuv` |
| Vigenère | `O'wfgpt vmw cv flqiy, hi guuifow xc yvi uuqh cyv uvlv` |
| SP-Network | `d'bpYgo hig mx bictv, av vqdyagc rv bma iacq axm tiii` |

---

## Paso 0 — Generación y normalización del dataset

### `generate_romance_dataset.py`

Construye el CSV inicial con textos literarios y filosóficos en ocho lenguas romances:
francés (`fr`), portugués (`pt`), italiano (`it`), rumano (`ro`), catalán (`ca`),
latín (`la`), gallego (`gl`) y occitano (`oc`).

El dataset fue expandido en etapas hasta alcanzar **2000 textos** únicos
(scripts auxiliares: `fill_to_1000.py`, `expand_to_1500.py`, `expand_to_2000.py`).

### `normalize_dataset.py`

Genera la columna `text_normalized` a partir de `text`:

- Expande ligaduras tipográficas (`œ → oe`, `æ → ae`, `ß → ss`, etc.)
- Descompone los caracteres con NFKD Unicode y elimina las marcas diacríticas
  (tildes, cedillas, diéresis, etc.)

Esto asegura que los algoritmos de cifrado, que operan sobre el alfabeto A-Z/a-z,
reciban únicamente letras ASCII sin caracteres especiales.

---

## Paso 1 — Cifrado César (`add_caesar.py`)

### Descripción del método

El **cifrado César** es un cifrado de sustitución monoalfabética donde cada letra
se desplaza un número fijo de posiciones en el alfabeto.

$$C = (P + k) \mod 26$$

donde $P$ es la posición de la letra original (0–25) y $k$ es el desplazamiento.

### Parámetros usados

| Parámetro | Valor |
|---|---|
| Desplazamiento (`shift`) | `3` |
| Entrada | `text_normalized` |
| Salida | columna `caesar` |

### Comportamiento

- Solo cifra letras (`isalpha()`); espacios, comas, apóstrofes, etc. se copian sin cambio.
- Respeta mayúsculas y minúsculas por separado.

### Ejemplo

```
Entrada:  Le coeur a ses raisons
Salida:   Oh frhxu d vhv udlvrqv
```

---

## Paso 2 — Cifrado Vigenère (`add_vigenere.py`)

### Descripción del método

El **cifrado Vigenère** es una extensión polialfabética del César: usa una clave
de varias letras, y cada letra del texto se desplaza según la letra correspondiente
de la clave (que se repite cíclicamente). Esto rompe la frecuencia uniforme del
César porque letras iguales en el texto pueden cifrarse de forma diferente.

$$C_i = (P_i + k_{i \bmod |key|}) \mod 26$$

donde $k_j = \text{ord}(\text{key}[j]) - \text{ord}(\text{'A'})$.

### Parámetros usados

| Parámetro | Valor |
|---|---|
| Clave (`KEY`) | `"AMOR"` |
| Entrada | columna `caesar` |
| Salida | columna `vigenere` |

### Comportamiento

- El índice de la clave avanza **únicamente con letras**; los caracteres no-alfabéticos
  no consumen posición de la clave.
- Conserva mayúsculas y minúsculas.

### Ejemplo

```
Entrada (César):   Oh frhxu d vhv udlvrqv txh od udlvrq qh frqqdlw srlqw
Clave repetida:    AM ORA M ORM ORAMORA MOR AM ORAMOR AM ORAMORA MORA
Salida (Vigenère): Ot tihji u vtj ldxjiqh hoh ar ldxjiq cv wrceuli gilck
```

---

## Paso 3 — Red de Sustitución-Permutación (`add_sp_network.py`)

### Descripción del método

Una **Red de Sustitución-Permutación (SP-Network)** es la estructura base de los
cifrados de bloque modernos (AES, entre otros). Combina dos operaciones:

1. **Sustitución (S-box)**: cada letra es reemplazada por otra usando una tabla fija.
   Introduce *confusión*, es decir, oculta la relación entre el texto y la clave.

2. **Permutación (P-box)**: los caracteres dentro de bloques de longitud fija se
   reordenan según un patrón determinista.
   Introduce *difusión*, es decir, distribuye la influencia de cada símbolo a lo
   largo del texto cifrado.

### Parámetros usados

| Parámetro | Valor |
|---|---|
| S-box | `"EKMFLGDQVZNTOWYHXUSPAIBRCJ"` |
| Tamaño de bloque | `8` letras |
| Patrón de permutación (`PERM`) | `[3, 1, 4, 0, 6, 2, 7, 5]` |
| Entrada | columna `vigenere` |
| Salida | columna `sp_network` |

### Cómo funciona la S-box

La S-box es un arreglo de 26 letras donde la posición `i` indica el reemplazo de la
letra `i`-ésima del alfabeto:

```
A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
E K M F L G D Q V Z N  T  O  W  Y  H  X  U  S  P  A  I  B  R  C  J
```

Se conserva la capitalización: una `a` minúscula se sustituye por la letra que le
corresponde en la S-box, pero en minúscula.

### Cómo funciona la permutación

Se trabaja solo con las letras del texto (ignorando espacios y puntuación).
Esas letras se dividen en bloques de 8. Dentro de cada bloque, las posiciones se
reordenan según el vector `PERM`:

```
PERM = [3, 1, 4, 0, 6, 2, 7, 5]
```

El valor en `PERM[i]` es la prioridad de la posición `i`; la posición con menor
prioridad pasa al slot 0 del bloque reordenado:

```
Posición original: 0  1  2  3  4  5  6  7
Prioridad PERM:    3  1  4  0  6  2  7  5
Orden resultante:  3→0, 1→1, 5→2, 0→3, 4→4 ...
                   (la letra en pos 3 va al slot 0, la de pos 1 al slot 1, etc.)
```

Una vez permutadas, las letras se reinsertan en las posiciones originales que
ocupaban en el texto (respetando dónde estaban los no-alfabéticos).

### Ejemplo

```
Entrada (Vigenère): Ot tihji u vtj ldxjiqh hoh ar ldxjiq cv wrceuli gilck
Tras S-box:         Vp paqav d tpr uzmavwq qyq eu umzavw mt ilmldua daumn  (aprox.)
Tras permutación:   vp zYpaq v tpr izvfzyq exq tq uvrmfz bx iamvulv tdmtn
```

---

## Reproducción completa del pipeline

Si se parte de cero (solo con el CSV inicial sin columnas de cifrado):

```bash
python normalize_dataset.py
python add_caesar.py
python add_vigenere.py
python add_sp_network.py
```

Cada script verifica que la columna de entrada exista y que la columna de salida
no haya sido creada previamente, abortando con un mensaje si alguna condición
no se cumple.
