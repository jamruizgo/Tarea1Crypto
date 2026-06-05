# Experimentación: Evaluación de LLMs en Descifrado

Experimento de descifrado progresivo con modelos de lenguaje de gran escala (LLMs).
Se evalúa la capacidad de cada modelo para descifrar textos procesados con un pipeline
de tres capas de cifrado: **César → Vigenère → Red de Sustitución-Permutación (SP-Network)**.

---

## 1. Objetivo

Medir si los LLMs pueden descifrar un texto cifrado con múltiples capas cuando:

- **Nivel 0 (Ciego)**: no reciben ninguna pista.
- **Nivel 1 (Métodos)**: se les indica cuáles algoritmos se usaron.
- **Nivel 2 (Orden + Llaves)**: se les indica el orden exacto y los parámetros de cada cifrado.

---

## 2. Modelos seleccionados

Se eligieron modelos de distintas familias, tamaños y proveedores para comparar
capacidades de razonamiento simbólico y criptoanálisis.

| ID | Modelo | Proveedor | Acceso |
|---|---|---|---|
| M1 | GPT-4o | OpenAI | API / ChatGPT |
| M2 | GPT-4o-mini | OpenAI | API |
| M3 | Claude 3.5 Sonnet | Anthropic | API / Claude.ai |
| M4 | Claude 3 Haiku | Anthropic | API |
| M5 | Gemini 1.5 Pro | Google | API / AI Studio |
| M6 | Gemini 1.5 Flash | Google | API |
| M7 | Llama 3.1 70B | Meta (vía Groq) | API gratuita |
| M8 | Mixtral 8x7B | Mistral (vía Groq) | API gratuita |

**Criterios de selección:**
- Al menos un modelo propietario SOTA por familia (OpenAI, Anthropic, Google).
- Un modelo de menor tamaño por familia como línea base interna.
- Dos modelos open-source para comparar con los propietarios sin costo.

---

## 3. Muestra de textos

Con 2000 textos en 8 lenguas (`fr`, `pt`, `it`, `ro`, `ca`, `la`, `gl`, `oc`),
usar el dataset completo para todos los modelos es costoso. Se propone:

| Estrategia | Descripción |
|---|---|
| **Muestra estratificada** | 20 textos por idioma × 8 idiomas = **160 textos** |
| **Selección** | Aleatorios con semilla fija (`random.seed(42)`) para reproducibilidad |
| **Longitud** | Incluir textos cortos (< 55 chars), medios (55–70) y largos (> 70) |

> Para una exploración rápida usar solo 10 textos por idioma (80 en total).
> Para resultados publicables usar los 160.

---

## 4. Niveles de pista y prompts

Cada texto pasa por los niveles de forma secuencial.
Solo se avanza al siguiente nivel si el modelo **no descifró correctamente** en el anterior.

---

### Nivel 0 — Sin pistas (Ciego)

El modelo recibe únicamente el texto cifrado y se le pide que lo descifre.

```
SYSTEM:
You are an expert cryptanalyst. Your task is to decrypt the given ciphertext
and return only the plaintext, with no explanation or additional commentary.
If you cannot decrypt it, respond with exactly: UNABLE_TO_DECRYPT

USER:
Decrypt the following ciphertext:

{sp_network}

Respond with only the decrypted text.
```

---

### Nivel 1 — Pista: métodos usados

Se revela que se usaron tres métodos, pero no el orden ni los parámetros.

```
SYSTEM:
You are an expert cryptanalyst. Your task is to decrypt the given ciphertext.
The text was encrypted using a combination of three classical methods:
- Caesar cipher
- Vigenère cipher
- Substitution-Permutation Network (S-box + block permutation)

Return only the plaintext with no explanation or commentary.
If you cannot decrypt it, respond with exactly: UNABLE_TO_DECRYPT

USER:
Decrypt the following ciphertext:

{sp_network}

Respond with only the decrypted text.
```

---

### Nivel 2 — Pista completa: orden + llaves + parámetros

Se revela el pipeline completo con todos los parámetros necesarios para la inversión exacta.

```
SYSTEM:
You are an expert cryptanalyst. The text was encrypted in this exact order:

STEP 1 — Caesar cipher
  - Shift: 3 (each letter moved 3 positions forward in the alphabet)
  - Non-alphabetic characters (spaces, punctuation) are unchanged

STEP 2 — Vigenère cipher (applied on top of Caesar output)
  - Key: "AMOR" (repeated cyclically)
  - Key index advances only on alphabetic characters
  - Case is preserved

STEP 3 — Substitution-Permutation Network (applied on top of Vigenère output)
  - S-box (A→Z mapping): EKMFLGDQVZNTOWYHXUSPAIBRCJ
    (position 0=A maps to E, position 1=B maps to K, etc.)
  - Block size: 8 letters
  - Permutation pattern PERM: [3, 1, 4, 0, 6, 2, 7, 5]
    (PERM[i] is the priority of position i; lower priority = earlier in output)
  - Only alphabetic characters participate in permutation; non-alphabetic stay in place
  - Case is preserved throughout

To decrypt, reverse the steps: invert SP-Network → invert Vigenère → invert Caesar.

Return only the final plaintext with no explanation or commentary.
If you cannot decrypt it, respond with exactly: UNABLE_TO_DECRYPT

USER:
Decrypt the following ciphertext:

{sp_network}

Respond with only the decrypted text.
```

---

## 5. Criterios de evaluación

Para cada intento se calculan tres métricas sobre el texto producido vs. `text_normalized`:

### 5.1 Exact Match (EM)
Coincidencia exacta carácter a carácter (sin distinguir mayúsculas).

$$EM = \begin{cases} 1 & \text{si } \hat{y} = y \\ 0 & \text{si no} \end{cases}$$

### 5.2 Character Error Rate (CER)
Distancia de edición a nivel de carácter, normalizada por la longitud del texto de referencia.

$$CER = \frac{\text{edit\_distance}(\hat{y},\, y)}{|y|}$$

Valores más bajos indican mejor desempeño. CER = 0 equivale a EM = 1.

### 5.3 Word-Level Accuracy (WA)
Porcentaje de palabras descifradas correctamente (comparación posicional).

$$WA = \frac{\text{palabras correctas}}{|\text{palabras en referencia}|}$$

---

## 6. Sistema de puntuación por texto

Cada texto recibe una puntuación de 0 a 3 según en qué nivel se logró descifrar:

| Nivel en que se descifró | Puntos |
|---|---|
| Nivel 0 (sin pistas) | 3 |
| Nivel 1 (métodos) | 2 |
| Nivel 2 (orden + llaves) | 1 |
| No descifrado en ningún nivel | 0 |

La **puntuación total** de un modelo es la suma de puntos sobre todos los textos de la muestra.
La **puntuación máxima** es `3 × N` (donde N = número de textos evaluados).

---

## 7. Diseño del experimento

### 7.1 Flujo por texto

```
Para cada texto t en la muestra:
  Para cada modelo M:
    Nivel 0:
      response = prompt_L0(t.sp_network)
      if correct(response, t.text_normalized):
        score[M][t] = 3 → continuar con siguiente texto
    Nivel 1:
      response = prompt_L1(t.sp_network)
      if correct(response, t.text_normalized):
        score[M][t] = 2 → continuar con siguiente texto
    Nivel 2:
      response = prompt_L2(t.sp_network)
      if correct(response, t.text_normalized):
        score[M][t] = 1 → continuar con siguiente texto
      else:
        score[M][t] = 0
```

### 7.2 Definición de "correcto"

Un intento se considera correcto si cumple **al menos una** de:
- EM = 1 (coincidencia exacta, case-insensitive), **o**
- CER ≤ 0.05 (≤ 5% de error de carácter, tolerando pequeñas variaciones de formato)

### 7.3 Temperatura y repeticiones

| Parámetro | Valor |
|---|---|
| Temperatura | `0.0` (salidas deterministas) |
| Top-p | `1.0` |
| Intentos por nivel | `1` (temperatura 0 hace redundante repetir) |
| Timeout por request | `60 s` |

---

## 8. Estructura de resultados

### 8.1 Por texto (`results_raw.csv`)

| Campo | Descripción |
|---|---|
| `id` | ID del texto del dataset |
| `language` | Idioma |
| `model` | ID del modelo (M1–M8) |
| `level_solved` | Nivel en que se descifró (0, 1, 2, o -1 si falló) |
| `score` | Puntos obtenidos (3, 2, 1, 0) |
| `cer_l0` / `cer_l1` / `cer_l2` | CER en cada nivel |
| `em_l0` / `em_l1` / `em_l2` | Exact Match en cada nivel |
| `response_l0` / `response_l1` / `response_l2` | Respuesta del modelo |

### 8.2 Resumen por modelo (`results_summary.csv`)

| Campo | Descripción |
|---|---|
| `model` | ID del modelo |
| `total_score` | Suma total de puntos |
| `max_score` | Puntuación máxima posible |
| `score_pct` | `total_score / max_score × 100` |
| `em_rate_l0` | % de textos con EM=1 en Nivel 0 |
| `em_rate_l1` | % adicionales con EM=1 en Nivel 1 |
| `em_rate_l2` | % adicionales con EM=1 en Nivel 2 |
| `avg_cer_l0` | CER promedio en Nivel 0 |
| `never_solved` | % de textos que ningún nivel resolvió |

---

## 9. Análisis propuestos

Una vez obtenidos los resultados, se sugieren los siguientes análisis:

1. **Ranking general**: tabla de modelos ordenada por `score_pct`.
2. **Por idioma**: ¿hay idiomas donde todos los modelos fallan más? (latín, occitano vs. francés, italiano).
3. **Por longitud**: ¿los textos más largos son más difíciles de descifrar?
4. **Curva de pistas**: gráfico de barras apiladas mostrando cuántos textos resolvió cada modelo en L0, L1 y L2.
5. **Análisis de error**: en los fallos del Nivel 2 (con todos los parámetros), ¿qué paso del descifrado falló? (comparar `caesar`, `vigenere`, `sp_network` intermedios).
6. **Correlación CER**: ¿los modelos con menor CER en L0 también tienen mayor EM en L2?

---

## 10. Implementación sugerida

### Dependencias

```bash
pip install openai anthropic google-generativeai groq pandas editdistance tqdm
```

### Estructura de archivos

```
cripto/
├── romance_dataset.csv
├── experiment/
│   ├── run_experiment.py      # script principal
│   ├── prompts.py             # plantillas de prompts L0, L1, L2
│   ├── metrics.py             # CER, EM, WA
│   ├── models.py              # wrappers para cada API
│   ├── sample.py              # selección de muestra estratificada
│   ├── results_raw.csv        # resultados por texto (generado)
│   └── results_summary.csv    # resumen por modelo (generado)
```

### Esqueleto de `run_experiment.py`

```python
import pandas as pd
import random
from prompts import L0, L1, L2
from metrics import is_correct, compute_cer
from models import query_model

MODELS = ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet", "claude-3-haiku",
          "gemini-1.5-pro", "gemini-1.5-flash", "llama-3.1-70b", "mixtral-8x7b"]

random.seed(42)
df = pd.read_csv("romance_dataset.csv")

# Muestra estratificada: 20 por idioma
sample = (df.groupby("language", group_keys=False)
            .apply(lambda g: g.sample(min(20, len(g)))))

records = []

for _, row in sample.iterrows():
    ciphertext = row["sp_network"]
    reference  = row["text_normalized"].lower().strip()

    for model in MODELS:
        result = {"id": row["id"], "language": row["language"], "model": model}
        solved = False

        for level, prompt_fn in enumerate([L0, L1, L2]):
            response = query_model(model, prompt_fn(ciphertext))
            cer      = compute_cer(response, reference)
            em       = int(response.lower().strip() == reference)

            result[f"response_l{level}"] = response
            result[f"cer_l{level}"]      = round(cer, 4)
            result[f"em_l{level}"]       = em

            if not solved and is_correct(response, reference):
                result["level_solved"] = level
                result["score"]        = 3 - level
                solved = True
                break  # no avanzar al siguiente nivel

        if not solved:
            result.setdefault("level_solved", -1)
            result.setdefault("score", 0)

        records.append(result)

pd.DataFrame(records).to_csv("experiment/results_raw.csv", index=False)
print("Experimento completado.")
```

### Esqueleto de `metrics.py`

```python
import editdistance

def compute_cer(hypothesis: str, reference: str) -> float:
    h = hypothesis.lower().strip()
    r = reference.lower().strip()
    if len(r) == 0:
        return 0.0
    return editdistance.eval(h, r) / len(r)

def is_correct(hypothesis: str, reference: str, cer_threshold: float = 0.05) -> bool:
    if hypothesis.strip().upper() == "UNABLE_TO_DECRYPT":
        return False
    cer = compute_cer(hypothesis, reference)
    return cer <= cer_threshold
```

---

## 11. Hipótesis esperadas

| Hipótesis | Justificación |
|---|---|
| Los modelos SOTA (GPT-4o, Claude 3.5 Sonnet) superarán al resto en L2 | Mayor capacidad de razonamiento simbólico paso a paso |
| Ningún modelo resolverá más del 5% de textos en L0 | El triple cifrado rompe toda frecuencia estadística reconocible |
| El CER en L1 disminuirá significativamente respecto a L0 | Nombrar los métodos activa conocimiento procedimental en el LLM |
| Los textos en latín y occitano serán los más difíciles en todos los niveles | Menor representación en los datos de preentrenamiento de los modelos |
| Los textos cortos (< 55 chars) tendrán menor tasa de éxito en L0 | Menos señal estadística para el criptoanálisis |
