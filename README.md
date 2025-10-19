# Hangman Solver Automat

Solver automat pentru jocul Hangman care identifică cuvinte pornind de la un pattern parțial cunoscut.

## 📋 Cerințe

- Python 3.7+
- Fără dependențe externe (rulare 100% offline)

## 🚀 Instalare și Rulare

### 1. Instalare dependențe
```bash
pip install -r requirements.txt
```

### 2. Generare fișier CSV de test
```bash
cd data
python convert_to_csv.py
```

### 3. Rulare solver
```bash
python solve_hangman.py --input data/test.csv --output results/output.csv
```

### Parametri CLI

| Parametru | Scurt | Descriere | Obligatoriu | Default |
|-----------|-------|-----------|-------------|---------|
| `--input` | `-i` | Fișier CSV de intrare | ✅ Da | - |
| `--output` | `-o` | Fișier CSV de ieșire | ✅ Da | - |
| `--max-iter` | - | Limită încercări per joc | ❌ Nu | 1200 |

### Exemple de utilizare

```bash
# Rulare standard
python solve_hangman.py --input data/test.csv --output results/out.csv

# Cu limită personalizată
python solve_hangman.py -i data/test.csv -o results/out.csv --max-iter 1500

# Format scurt
python solve_hangman.py -i data/test.csv -o results/out.csv
```

## 📁 Structura Proiectului

```
proiect-main/
├── data/
│   ├── test.csv                    # Fișier CSV de intrare
│   ├── cuvinte_de_verificat.txt    # Fișier original (format txt)
│   └── convert_to_csv.py           # Script conversie txt → CSV
├── src/
│   └── hangman.py                  # Algoritm solver
├── results/
│   └── output.csv                  # Rezultate (generat)
├── docs/
│   └── prezentare.pptx             # Prezentare proiect
├── solve_hangman.py                # Script principal CLI
├── test_solver.py                  # Script pentru testare (opțional)
├── requirements.txt                # Dependențe Python
└── README.md                       # Documentație
```

## 📊 Format Fișiere

### Input CSV (obligatoriu)

**Coloane:** `game_id`, `pattern_initial`, `cuvant_tinta`

**Exemplu:**
```csv
game_id,pattern_initial,cuvant_tinta
1,******RA**,ICONOGRAFĂ
2,*A**C****,FAGOCITUL
3,**T*ST,ATTEST
```

**Convenții:**
- Separator: `,` (virgulă)
- Encoding: UTF-8
- `*` = literă necunoscută
- Litere cunoscute = litere din cuvânt (case-insensitive)
- Suport diacritice românești: `ă â î ș ț`

### Output CSV (generat automat)

**Coloane:** `game_id`, `total_incercari`, `cuvant_gasit`, `status`, `secventa_incercari`

**Exemplu:**
```csv
game_id,total_incercari,cuvant_gasit,status,secventa_incercari
1,25,ICONOGRAFĂ,OK,"E, A, I, R, O, N, C, G, F"
2,18,FAGOCITUL,OK,"E, A, I, O, G, C, T, U, L"
INVALID,0,N/A,FAIL,""
```

**Câmpuri:**
- `game_id`: ID unic al jocului
- `total_incercari`: Număr total de litere încercate
- `cuvant_gasit`: Cuvântul identificat (sau `N/A` dacă a eșuat)
- `status`: `OK` (success) sau `FAIL` (eșec)
- `secventa_incercari`: Liste de litere separate prin virgulă

## ✅ Validare Input

Scriptul validează automat fiecare linie din CSV și raportează erori:

### Validări efectuate:

1. **Câmpuri lipsă**: Toate coloanele trebuie completate
2. **Lungimi diferite**: `len(pattern_initial) == len(cuvant_tinta)`
3. **Pattern inconsistent**: Literele din pattern trebuie să corespundă cu target
4. **Caractere invalide**: Doar litere și `*` sunt permise

### Erori raportate:

```
⚠️ ERORI DE VALIDARE (3):
  [Linia 4] Game ID 'INVALID1': LENGTH_MISMATCH - Lungimi diferite: pattern=3 vs target=8
  [Linia 5] Game ID 'INVALID2': MISSING_FIELD - pattern_initial lipsește
  [Linia 7] Game ID 'BAD_PATTERN': PATTERN_MISMATCH - Pattern inconsistent: poziția 2, pattern='*' dar target='B'
```

Liniile invalide sunt **omise** din procesare și raportate la final.

## 🎯 Algoritm Solver

### Strategie

1. **Frecvență litere românești**: Prioritizează litere comune (E, A, I, R, T...)
2. **Biograme românești**: Identifică perechi frecvente (RE, LE, AR, DE...)
3. **Analiza pattern-ului**: Scorare contextuală pe baza literelor cunoscute
4. **Gap filling**: Completare automată pentru goluri mici (≤2 litere)

### Performanță

- **Limită obligatorie**: Suma totală < 1200 încercări pentru toate jocurile
- **Acuratețe**: 100% (toate cuvintele trebuie identificate corect)
- **Timp execuție**: < 180s (recomandat)

## 📈 Raport Final

La finalizare, scriptul afișează un raport complet:

```
############################################################
RAPORT FINAL
############################################################

📋 VALIDARE:
  Linii totale procesate: 103
  Linii valide: 100
  Linii invalide (omise): 3

⚠️ ERORI DE VALIDARE (3):
  [Linia 45] Game ID 'TEST1': LENGTH_MISMATCH - Lungimi diferite...

🎯 REZULTATE:
  Jocuri rezolvate (OK): 100/100
  Jocuri eșuate (FAIL): 0/100
  Rată de succes: 100.00%
  Total încercări: 1156
  ✅ PERFORMANȚĂ: Sub limita de 1200 încercări!

⏱️ Timp de execuție: 42.35 secunde
```

## 🔧 Limitări și Ipoteze

### Ipoteze
- Toate cuvintele sunt în limba română
- Diacriticele sunt corecte în input
- Pattern-ul inițial este consistent cu cuvântul target

### Limitări
- Nu suportă cuvinte cu caractere speciale (cifre, semne de punctuație)
- Performanță dependentă de complexitatea cuvintelor
- Nu folosește dicționar extern (doar frecvență și biograme)

## 📝 Definiții

- **Încercare**: O propunere de literă
- **Joc rezolvat**: `cuvant_gasit == cuvant_tinta`
- **Total încercări**: Suma tuturor încercărilor din toate jocurile
- **Status OK**: Cuvânt identificat corect
- **Status FAIL**: Eșec în identificare (limită depășită sau eroare)

## 🛠️ Dezvoltare și Testare

### Rulare teste
```bash
python test_solver.py
```

### Testare validare
```bash
python solve_hangman.py -i data/test_validation.csv -o results/validation_out.csv
```

## 📚 Resurse

- Frecvențe litere românești: Bazat pe corpus Romanian Language
- Biograme: Analiză statistică limba română
- Pattern matching: Implementare proprie

## 👥 Autor

Proiect realizat pentru cursul de [Practica de Specialitate] - [UTCN Baia Mare]

