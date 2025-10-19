import random
import time
import csv
from typing import Optional, Tuple, List, Set

ROMANIAN_LETTER_FREQUENCY: List[str] = [ #31
    'E', 'A', 'I', 'R', 'T', 'N', 'U', 'L', 'O', 'S',
    'C', 'D', 'P', 'M', 'Ă', 'V', 'F', 'B', 'G', 'Î',
    'H', 'Ț', 'Ș', 'Z', 'Â', 'J', 'K', 'W', 'X', 'Y', 'Q'
]

ROMANIAN_BIGRAMS: List[str] = [
    'RE', 'LE', 'RI', 'RA', 'TE', 'EA', 'AR', 'OR', 'DE',
    'IN', 'EN', 'LA', 'AL', 'TU', 'NE', 'RU', 'CA', 'SE',
    'ER', 'IL', 'AT', 'ES', 'RO', 'AN', 'CE', 'ÎN', 'PE',
    'NT', 'ST', 'TR', 'PR', 'BR', 'CR', 'DR', 'FR', 'GR',
    'PL', 'BL', 'CL', 'FL', 'GL', 'TA', 'TI', 'TO'
]


def load_all_games_from_csv(filename: str) -> List[Tuple[str, str, str]]:
    """
    Încarcă toate jocurile din fișierul CSV
    Returns: Lista de (game_id, pattern_initial, cuvant_tinta)
    """
    games = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                game_id = row.get('game_id', '').strip()
                pattern_initial = row.get('pattern_initial', '').strip()
                cuvant_tinta = row.get('cuvant_tinta', '').strip().upper()
                
                if all([game_id, pattern_initial, cuvant_tinta]):
                    games.append((game_id, pattern_initial, cuvant_tinta))
                else:
                    print(f"⚠️  Linie incompletă ignorată: {row}")
            
        return games
    
    except FileNotFoundError:
        print(f"❌ Fișierul {filename} nu a fost găsit!")
        return []
    except Exception as e:
        print(f"❌ Eroare la citirea CSV: {e}")
        return []


def write_results_to_csv(results: List[dict], output_filename: str):
    """
    Scrie rezultatele în fișier CSV
    """
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['game_id', 'total_incercari', 'cuvant_gasit', 'status', 'secventa_incercari']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✅ Rezultate salvate în: {output_filename}")
    except Exception as e:
        print(f"❌ Eroare la salvare: {e}")


def display_current_state(word: str, guessed_letters: Set[str]) -> str:
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display


def get_letter_positions(word: str, letter: str) -> List[int]:
    positions = []
    for i, char in enumerate(word):
        if char == letter:
            positions.append(i) 
    return positions

# Crearea scorului pe baza a frecventei literei cat si a cat de des este intalnita
def get_pattern_score(letter: str, current_state: str, word_length: int, guessed_letters: Set[str]) -> int:
    score = 0
    vowels = ['A', 'E', 'I', 'O', 'U', 'Ă', 'Â', 'Î']
    
    if letter in ROMANIAN_LETTER_FREQUENCY:
        position = ROMANIAN_LETTER_FREQUENCY.index(letter)
        score += (len(ROMANIAN_LETTER_FREQUENCY) - position) * 5
    
    if letter in vowels:
        score += 100
    
    for i, char in enumerate(current_state):
        if char == letter and char != '_':
            score += 50
    
    for i, char in enumerate(current_state):
        if char != '_':
            if i > 0 and current_state[i-1] == '_':
                potential_bigram = letter + char
                if potential_bigram in ROMANIAN_BIGRAMS:
                    score += 40
            
            if i < word_length - 1 and current_state[i+1] == '_':
                potential_bigram = char + letter
                if potential_bigram in ROMANIAN_BIGRAMS:
                    score += 40
    
    return score

# Vecinii exista = Cauta biograme
def find_missing_letter_in_gap(current_state: str, guessed_letters: Set[str]) -> Optional[str]:
    for i, char in enumerate(current_state):
        if char == '_':
            before = current_state[i-1] if i > 0 else None
            after = current_state[i+1] if i < len(current_state)-1 else None
            
            if before and after and before != '_' and after != '_':
                for letter in ROMANIAN_LETTER_FREQUENCY:
                    if letter in guessed_letters:
                        continue
                    
                    bigram_left = before + letter
                    bigram_right = letter + after
                    
                    if bigram_left in ROMANIAN_BIGRAMS and bigram_right in ROMANIAN_BIGRAMS:
                        return letter
    return None

# Crearea noii liste pentru lipsa<=2 
def choose_next_letter_advanced(guessed_letters: Set[str], current_state: str, word_length: int) -> Optional[str]:
    available_letters = [letter for letter in ROMANIAN_LETTER_FREQUENCY if letter not in guessed_letters]
    
    if not available_letters:
        return None
    
    missing_count = current_state.count('_')
    if missing_count <= 2 and missing_count > 0:
        gap_letter = find_missing_letter_in_gap(current_state, guessed_letters)
        if gap_letter:
            return gap_letter # Ca sa nu returneze None. 
    
    letter_scores = {}
    for letter in available_letters:
        score = get_pattern_score(letter, current_state, word_length, guessed_letters)
        letter_scores[letter] = score
    
    best_letter = max(letter_scores, key=letter_scores.get)
    return best_letter


def solve_hangman_silent(encoded: str, actual_word: str, max_iterations: int = 1200) -> Tuple[bool, int, int, int, List[str]]:
    """
    Versiune silențioasă a solver-ului pentru procesare batch
    Nu afișează nimic, doar returnează rezultatele
    """
    word_length = len(actual_word)
    actual_word = actual_word.upper()
    guessed_letters = set()
    wrong_guesses = 0
    attempts = 0
    sequence_of_attempts = []
    
    # Inițializare state din pattern
    for i, char in enumerate(encoded.upper()):
        if char != '*':
            guessed_letters.add(char)
    
    current_state = display_current_state(actual_word, guessed_letters)
    
    while current_state != actual_word and attempts < max_iterations:
        attempts += 1
        
        next_letter = choose_next_letter_advanced(guessed_letters, current_state, word_length)
        
        if next_letter is None:
            return False, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts
        
        guessed_letters.add(next_letter)
        sequence_of_attempts.append(next_letter)
        
        positions = get_letter_positions(actual_word, next_letter)
        
        if positions:
            current_state = display_current_state(actual_word, guessed_letters)
        else:
            wrong_guesses += 1
    
    # Returnează rezultatul
    if current_state == actual_word:
        return True, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts
    else:
        return False, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts


def solve_hangman(encoded: str, actual_word: str, max_iterations: int = 1200, delay: float = 0.5) -> Tuple[bool, int, int, int, List[str]]:
    word_length = len(actual_word)
    guessed_letters = set()
    wrong_guesses = 0
    attempts = 0
    sequence_of_attempts = []  # Lista cu secvența încercărilor
    
    print("=" * 60)
    print("HANGMAN AUTOMAT - SOLVER (Advanced)")
    print("=" * 60)
    print(f"\nCuvant de ghicit (lungime: {word_length})")
    print(f"Limita maxima de incercari: {max_iterations}")
    print(f"\nStare initiala: {encoded}")
    print("\n" + "-" * 60)
    
    current_state = display_current_state(actual_word, guessed_letters)
    print(f"\nStare curenta: {current_state}")
    
    while current_state != actual_word and attempts < max_iterations:
        attempts += 1
        
        next_letter = choose_next_letter_advanced(guessed_letters, current_state, word_length)
        
        if next_letter is None:
            print("\nNu mai sunt litere de încercat!")
            return False, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts
        
        guessed_letters.add(next_letter)
        sequence_of_attempts.append(next_letter)  # Adaugă litera în secvență
        
        positions = get_letter_positions(actual_word, next_letter)
        
        time.sleep(delay) 
        
        if positions:
            print(f"\n[Incercarea #{attempts}] Litera: '{next_letter}' GASITA")
            print(f"   -> Pozitii: {[p+1 for p in positions]}")
            current_state = display_current_state(actual_word, guessed_letters)
            print(f"   -> Stare noua: {current_state}")
        else:
            wrong_guesses += 1
            print(f"\n[Incercarea #{attempts}] Litera: '{next_letter}' NU ESTE")
            print(f"   -> Greseli totale: {wrong_guesses}")
            print(f"   -> Stare: {current_state}")

    print("\n" + "=" * 60)
    if current_state == actual_word:
        print("SUCCESS! Cuvant ghicit!")
        print(f"\nCuvant: {actual_word}")
        print(f"Incercari: {attempts} / {max_iterations}")
        print(f"Greseli: {wrong_guesses}")
        print(f"Litere incercate: {len(guessed_letters)}")
        print(f"Eficienta: {(attempts/max_iterations)*100:.2f}% din limita")
        return True, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts
    else:
        print("FAILED! Nu am ghicit cuvantul.")
        print(f"\nCuvant corect: {actual_word}")
        print(f"Am ajuns la: {current_state}")
        print(f"Incercari: {attempts} / {max_iterations}")
        print(f"Greseli: {wrong_guesses}")
        return False, attempts, wrong_guesses, len(guessed_letters), sequence_of_attempts


def main() -> None:
    import os
    
    # Determină directorul proiectului (părinte al directorului src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    
    # Căi absolute către fișiere
    csv_filename = os.path.join(project_dir, "data", "cuvinte_de_verificat.csv")
    output_filename = os.path.join(project_dir, "results", "hangman_results.csv")
    
    print("🎯 HANGMAN SOLVER - PROCESARE COMPLETĂ CSV")
    print("=" * 60)
    
    # Încărcăm toate jocurile din CSV
    print("📖 Încărcare jocuri din CSV...")
    games = load_all_games_from_csv(csv_filename)
    
    if not games:
        print("❌ Nu s-au găsit jocuri valide în CSV!")
        return
    
    print(f"✅ Încărcate {len(games)} jocuri")
    
    results = []
    total_attempts = 0
    successful_games = 0
    
    print("\n🚀 PROCESARE JOCURI:")
    print("=" * 60)
    
    for i, (game_id, pattern_initial, cuvant_tinta) in enumerate(games, 1):
        print(f"\n[{i}/{len(games)}] Game ID: {game_id}")
        print(f"   Pattern: {pattern_initial}")
        print(f"   Target: {cuvant_tinta}")
        
        # Rulează solver-ul silențios
        success, attempts, wrong_guesses, letters_tried, sequence = solve_hangman_silent(
            pattern_initial, cuvant_tinta, max_iterations=1200
        )
        
        # Pregătește rezultatul
        status = "OK" if success else "FAIL"
        cuvant_gasit = cuvant_tinta if success else "N/A"
        secventa_incercari = ", ".join(sequence)
        
        result = {
            'game_id': game_id,
            'total_incercari': attempts,
            'cuvant_gasit': cuvant_gasit,
            'status': status,
            'secventa_incercari': secventa_incercari
        }
        
        results.append(result)
        total_attempts += attempts
        if success:
            successful_games += 1
        
        print(f"   → Status: {status} | Încercări: {attempts} | Litere: {letters_tried}")
    
    # Salvează rezultatele
    print(f"\n💾 Salvare rezultate...")
    
    # Creează directorul results dacă nu există
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    write_results_to_csv(results, output_filename)
    
    # Raport final
    print(f"\n📊 RAPORT FINAL:")
    print("=" * 60)
    print(f"📋 Jocuri procesate: {len(games)}")
    print(f"✅ Jocuri rezolvate: {successful_games}/{len(games)} ({(successful_games/len(games)*100):.1f}%)")
    print(f"❌ Jocuri eșuate: {len(games)-successful_games}")
    print(f"� Total încercări: {total_attempts}")
    print(f"📈 Media încercări/joc: {total_attempts/len(games):.1f}")
    
    if total_attempts < 1200:
        print(f"🎉 PERFORMANȚĂ: Sub limita de 1200 încercări!")
    else:
        print(f"⚠️  PERFORMANȚĂ: Peste limita de 1200 încercări (+{total_attempts-1200})")
    
    print("=" * 60)
    print("🏁 Program finalizat.")
    print("=" * 60)


if __name__ == "__main__":
    main() # Initializare doar la ce trebuie.
