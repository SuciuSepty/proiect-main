# Hangman Solver Automat

Solver automat pentru jocul Hangman care identifică cuvinte pornind de la un pattern parțial cunoscut.

## ⚡ Start Rapid

```bash
# Clonează repository-ul
git clone <url-repository>
cd proiect-main

# Rulează solver-ul (FĂRĂ parametri!)
python src/hangman.py
```

**Rezultat:** Procesează automat 100 jocuri și salvează rezultatele în `results/hangman_results.csv`

## 📋 Cerințe

- Python 3.7+
- Fără dependențe externe (rulare 100% offline)

## 🚀 Instalare și Rulare

### 1. Instalare dependențe
```bash
pip install -r requirements.txt
```
*Notă: Fișierul requirements.txt este gol - proiectul rulează 100% offline fără dependențe externe.*

### 2. Rulare solver (SIMPLU - UN SINGUR COMMAND)
```bash
python src/hangman.py
```

**Atât!** Scriptul:
- ✅ Citește automat din `data/cuvinte_de_verificat.csv`
- ✅ Procesează toate jocurile (100)
- ✅ Salvează rezultatele în `results/hangman_results.csv`
- ✅ Afișează raport complet la final

### Rulare din orice director

```bash
# Din directorul principal
python src/hangman.py

# Sau din directorul src
cd src
python hangman.py

# Sau cu calea completă
python "C:\calea\ta\proiect-main\src\hangman.py"
```

## 📁 Structura Proiectului

```
proiect-main/
├── data/
│   ├── cuvinte_de_verificat.csv    # 📥 INPUT: Fișier CSV cu jocurile (100)
│   ├── cuvinte_de_verificat.txt    # Legacy (nu se mai folosește)
│   └── convert_to_csv.py           # Script conversie txt → CSV
├── src/
│   └── hangman.py                  # 🎯 MAIN: Tot codul aici (autonom)
├── results/
│   └── hangman_results.csv         # 📤 OUTPUT: Rezultate (generat automat)
├── requirements.txt                # Dependențe (gol - offline)
└── README.md                       # Documentație
```

**Fișiere importante:**
- **`src/hangman.py`** - Scriptul principal care face totul
- **`data/cuvinte_de_verificat.csv`** - Datele de intrare (100 jocuri)
- **`results/hangman_results.csv`** - Rezultatele generate

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

### Output CSV (generat automat în `results/hangman_results.csv`)

**Coloane:** `game_id`, `total_incercari`, `cuvant_gasit`, `status`, `secventa_incercari`

**Exemplu real din rezultate:**
```csv
game_id,total_incercari,cuvant_gasit,status,secventa_incercari
1,17,ICONOGRAFĂ,OK,"E, O, T, I, U, N, L, Ă, Î, C, D, P, Â, F, S, B, G"
2,19,FAGOCITUL,OK,"E, R, I, L, U, T, O, Ă, N, Î, Â, S, D, P, M, V, F, B, G"
3,10,APICOLILOR,OK,"E, A, I, U, R, O, T, Ă, N, L"
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

### Rezultate Obținute

✅ **Acuratețe**: 100/100 jocuri rezolvate (100%)  
📊 **Total încercări**: 1703 (peste limita de 1200)  
⏱️ **Timp execuție**: ~0.14 secunde  
📈 **Media per joc**: 17.0 încercări

## 📈 Raport Final

La finalizare, scriptul afișează un raport complet:

```
📊 RAPORT FINAL:
============================================================
📋 Jocuri procesate: 100
✅ Jocuri rezolvate: 100/100 (100.0%)
❌ Jocuri eșuate: 0
🔢 Total încercări: 1703
📈 Media încercări/joc: 17.0
⚠️  PERFORMANȚĂ: Peste limita de 1200 încercări (+503)
============================================================
🏁 Program finalizat.
```

**Interpretare:**
- ✅ **100% acuratețe** - toate cuvintele identificate corect
- ⚠️ **1703 încercări totale** - peste limita recomandată de 1200
- ⏱️ **~0.14 secunde** - execuție foarte rapidă
- 📁 **Rezultate salvate** automat în `results/hangman_results.csv`

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

### Rulare rapidă pentru testare
```bash
# Rulare completă (toate 100 jocurile)
python src/hangman.py

# Verificare rezultate
type results\hangman_results.csv  # Windows
# sau
cat results/hangman_results.csv   # Linux/Mac
```

### Modificare algoritm
Pentru a modifica strategia de rezolvare, editează fișierul `src/hangman.py`:
- **Funcția principală**: `solve_hangman_silent()`
- **Strategia de alegere**: `choose_next_letter_advanced()`
- **Scorarea literelor**: `get_pattern_score()`

## 📚 Resurse

- Frecvențe litere românești: Bazat pe corpus Romanian Language
- Biograme: Analiză statistică limba română
- Pattern matching: Implementare proprie

## 📄 Licență

Acest proiect este realizat în scop educațional.
