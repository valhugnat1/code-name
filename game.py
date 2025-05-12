import random
# Pour utiliser l'API OpenAI, vous devez l'installer : pip install openai
# et configurer votre clé API (par exemple via une variable d'environnement OPENAI_API_KEY)
# import openai
from openai import OpenAI # Utilisation recommandée pour les versions récentes

class Game:
    """
    Représente une partie du jeu de type Codenames.
    Gère le plateau de jeu, les tours des joueurs, les devinettes et la condition de victoire.
    """
    BOARD_SIZE = 5

    def __init__(self):
        """Initialise une nouvelle partie."""
        print("Initialisation d'une nouvelle partie...")

        # Initialisation des matrices vides
        # Matrice stockant les couleurs cachées ('red', 'blue', 'neutral', 'assassin')
        self.color_matrix = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        # Matrice stockant les mots sur le plateau
        self.word_matrix = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        # Matrice indiquant si une carte a été révélée (True) ou non (False)
        self.revealed_matrix = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        # Scores des équipes
        self.red_score = 0
        self.blue_score = 0

        # Détermination du joueur qui commence et du nombre total de cartes par couleur
        if random.choice([True, False]):
            self.current_player = 'red'
            self.red_cards_total = 9
            self.blue_cards_total = 8
            print("L'équipe ROUGE commence.")
        else:
            self.current_player = 'blue'
            self.red_cards_total = 8
            self.blue_cards_total = 9
            print("L'équipe BLEUE commence.")
        print(f"Objectif : {self.red_cards_total} cartes pour ROUGE, {self.blue_cards_total} cartes pour BLEU.")

        # Initialisation des matrices (avec placeholders pour votre code)
        self._initialize_color_matrix()
        self._initialize_word_matrix()

        self.game_over = False
        self.winner = None

    def _initialize_color_matrix(self):
        """
        Méthode pour initialiser la matrice des couleurs.
        !!! REMPLACEZ CE CODE PAR VOTRE LOGIQUE D'INITIALISATION !!!
        Doit remplir self.color_matrix avec 'red', 'blue', 'neutral', 'assassin'.
        Assurez-vous que le nombre de cartes rouges/bleues correspond à
        self.red_cards_total et self.blue_cards_total.
        Il doit y avoir 1 assassin et le reste en 'neutral'.
        """
        print("Initialisation de la matrice des couleurs (placeholder)...")
        # --- DÉBUT DE VOTRE CODE POUR INITIALISER LES COULEURS ---
        # Exemple simple de placeholder (distribution non aléatoire pour test) :
        colors = ['red'] * self.red_cards_total + \
                 ['blue'] * self.blue_cards_total + \
                 ['assassin'] * 1
        neutral_count = self.BOARD_SIZE * self.BOARD_SIZE - len(colors)
        colors += ['neutral'] * neutral_count
        random.shuffle(colors) # Mélange les couleurs

        k = 0
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                self.color_matrix[r][c] = colors[k]
                k += 1
        # --- FIN DE VOTRE CODE POUR INITIALISER LES COULEURS ---
        print("Matrice des couleurs initialisée.")
        # print(self.color_matrix) # Décommentez pour vérifier

    def _initialize_word_matrix(self):
        """
        Méthode pour initialiser la matrice des mots.
        !!! REMPLACEZ CE CODE PAR VOTRE LOGIQUE D'INITIALISATION !!!
        Doit remplir self.word_matrix avec les mots du jeu.
        """
        print("Initialisation de la matrice des mots (placeholder)...")
        # --- DÉBUT DE VOTRE CODE POUR INITIALISER LES MOTS ---
        # Exemple simple de placeholder :

        words = [
            "LUNE", "CHEVAL", "PIRATE", "MIROIR", "CHOCOLAT",
            "ROBOT", "PLAGE", "VAMPIRE", "TOUR", "FEU",
            "AVION", "BANANE", "NEIGE", "BANQUIER", "DRAGON",
            "SOURIS", "BIBLIOTHÈQUE", "COEUR", "NUAGE", "TRAIN",
            "FUSÉE", "TÉLÉPHONE", "MAGIE", "SOLDAT", "FORÊT"
        ]
        
        random.shuffle(words)
        k = 0
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                self.word_matrix[r][c] = words[k]
                k += 1
        # --- FIN DE VOTRE CODE POUR INITIALISER LES MOTS ---
        print("Matrice des mots initialisée.")
        # self.display_board(show_colors=False) # Décommentez pour vérifier

    def _get_remaining_words(self, color):
        """
        Retourne la liste des mots non découverts pour une couleur donnée.
        Utilise les trois matrices : word_matrix, color_matrix, revealed_matrix.
        """
        remaining = []
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if self.color_matrix[r][c] == color and not self.revealed_matrix[r][c]:
                    remaining.append(self.word_matrix[r][c])
        return remaining

    def _get_all_unrevealed_words(self):
        """Retourne la liste de tous les mots non découverts sur le plateau."""
        unrevealed = []
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if not self.revealed_matrix[r][c]:
                    unrevealed.append(self.word_matrix[r][c])
        return unrevealed

    def get_clue(self):
        """
        Obtient un indice (mot-clé et nombre) pour le joueur actuel.
        Actuellement, simule l'appel LLM en demandant à l'utilisateur.
        !!! MODIFIEZ CETTE FONCTION POUR UTILISER L'API OPENAI !!!
        """
        print(f"\n--- Tour de l'espion {self.current_player.upper()} ---")
        target_words = self._get_remaining_words(self.current_player)
        all_unrevealed_words = self._get_all_unrevealed_words()

        print(f"Mots restants pour {self.current_player.upper()} : {', '.join(target_words)}")
        print(f"Tous les mots non révélés : {', '.join(all_unrevealed_words)}")

        # --- DÉBUT DE LA SECTION POUR L'APPEL LLM OPENAI ---
        try:
            # Assurez-vous que la clé API est configurée (variable d'environnement, etc.)
            client = OpenAI() # Initialise le client OpenAI
        
            prompt = (
                f"Vous êtes l'espion de l'équipe {self.current_player} dans une partie de Codenames.\n"
                f"Voici les mots que votre équipe doit deviner : {', '.join(target_words)}\n"
                f"Voici tous les mots actuellement sur le plateau : {', '.join(all_unrevealed_words)}\n"
                f"Donnez un indice sous la forme 'MOT, CHIFFRE' où MOT est un seul mot qui n'est PAS sur le plateau "
                f"et CHIFFRE est le nombre de mots de votre équipe ({self.current_player}) qui sont liés à MOT. "
                f"Ne donnez que le MOT et le CHIFFRE séparés par une virgule."
            )
        
            response = client.chat.completions.create(
                model="gpt-4o", # Ou un autre modèle approprié
                messages=[{"role": "system", "content": prompt}],
                max_tokens=10,
                temperature=0.5
            )
            clue_text = response.choices[0].message.content.strip()
        
            # Traitement de la réponse (exemple simple)
            parts = clue_text.split(',')
            if len(parts) == 2:
                keyword = parts[0].strip().upper()
                try:
                    number = int(parts[1].strip())
                    if keyword not in all_unrevealed_words: # Vérification supplémentaire
                         print(f"Indice reçu de l'IA : {keyword}, {number}")
                         return keyword, number
                    else:
                         print("Erreur : L'IA a donné un mot présent sur le plateau.")
                except ValueError:
                    print("Erreur : L'IA n'a pas retourné un chiffre valide.")
            else:
                 print("Erreur : Format de réponse inattendu de l'IA.")
        
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API OpenAI : {e}")
            print("Passage à la saisie manuelle de l'indice.")

        # --- FIN DE LA SECTION POUR L'APPEL LLM OPENAI ---

        # Solution de repli : Saisie manuelle de l'indice
        while True:
            try:
                clue_input = input(f"Espion {self.current_player.upper()}, entrez votre indice (Mot, Chiffre) : ")
                keyword, number_str = clue_input.split(',')
                keyword = keyword.strip().upper()
                number = int(number_str.strip())
                if number < 1:
                    print("Le chiffre doit être au moins 1.")
                    continue
                # Vérification simple que l'indice n'est pas un mot du plateau
                # (une vérification plus robuste comparerait avec word_matrix directement)
                is_on_board = False
                for r in range(self.BOARD_SIZE):
                  for c in range(self.BOARD_SIZE):
                    if self.word_matrix[r][c].upper() == keyword:
                      is_on_board = True
                      break
                  if is_on_board:
                    break
                if is_on_board:
                     print(f"Erreur : Le mot '{keyword}' est déjà sur le plateau.")
                     continue

                return keyword, number
            except ValueError:
                print("Format invalide. Utilisez 'Mot, Chiffre'. Exemple : 'Animal, 3'")
            except Exception as e:
                 print(f"Une erreur inattendue est survenue: {e}")


    def _find_word_coords(self, word_guess):
        """Trouve les coordonnées (ligne, colonne) d'un mot dans word_matrix."""
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if self.word_matrix[r][c].upper() == word_guess.upper():
                    return r, c
        return None # Mot non trouvé

    def make_guess(self):
        """
        Gère la devinette d'un mot par l'équipe actuelle.
        Retourne:
            True si le joueur peut continuer à deviner.
            False si le tour du joueur se termine (erreur, neutre, adversaire, assassin).
            'WIN' si la devinette a fait gagner l'équipe.
            'LOSS' si la devinette a fait perdre l'équipe (assassin).
        """
        while True:
            guess = input(f"Équipe {self.current_player.upper()}, quel mot choisissez-vous ? (ou 'PASSE') ").strip().upper()

            if guess == 'PASSE':
                print("L'équipe passe son tour.")
                return False # Termine le tour

            coords = self._find_word_coords(guess)

            if coords is None:
                print(f"Le mot '{guess}' n'est pas sur le plateau. Essayez encore.")
                continue # Demande une nouvelle saisie

            r, c = coords
            if self.revealed_matrix[r][c]:
                print(f"Le mot '{guess}' a déjà été révélé. Essayez encore.")
                continue # Demande une nouvelle saisie

            # Révéler la carte
            self.revealed_matrix[r][c] = True
            revealed_color = self.color_matrix[r][c]
            revealed_word = self.word_matrix[r][c] # Garde la casse originale
            print(f" -> '{revealed_word}' est de couleur : {revealed_color.upper()}")

            if revealed_color == self.current_player:
                if self.current_player == 'red':
                    self.red_score += 1
                else:
                    self.blue_score += 1
                print(f"Correct ! Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")
                if self._check_win_condition():
                    return 'WIN' # Le joueur gagne
                return True # Peut continuer à deviner

            elif revealed_color == 'neutral':
                print("C'est une carte neutre.")
                return False # Termine le tour

            elif revealed_color == 'assassin':
                print("Oh non ! C'est l'assassin !")
                self.game_over = True
                self.winner = 'red' if self.current_player == 'blue' else 'blue' # L'autre joueur gagne
                print(f"L'équipe {self.winner.upper()} gagne !")
                return 'LOSS' # Le joueur perd

            else: # C'est une carte de l'adversaire
                if revealed_color == 'red':
                    self.red_score += 1
                else:
                    self.blue_score += 1
                print(f"C'est une carte de l'équipe adverse ! Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")
                if self._check_win_condition(): # L'adversaire pourrait gagner
                     # La condition de victoire sera gérée à la fin du tour ou au début du suivant
                     pass
                return False # Termine le tour

    def _check_win_condition(self):
        """Vérifie si une condition de victoire est atteinte."""
        if self.red_score >= self.red_cards_total:
            self.game_over = True
            self.winner = 'red'
            return True
        if self.blue_score >= self.blue_cards_total:
            self.game_over = True
            self.winner = 'blue'
            return True
        return False

    def _switch_player(self):
        """Change le joueur actuel."""
        self.current_player = 'blue' if self.current_player == 'red' else 'red'

    def display_board(self, show_colors=False):
        """Affiche le plateau de jeu dans la console."""
        print("\n--- PLATEAU DE JEU ---")
        col_width = 15 # Largeur de colonne pour l'affichage
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                word = self.word_matrix[r][c]
                if self.revealed_matrix[r][c]:
                    color = self.color_matrix[r][c]
                    # Affiche le mot et sa couleur (en majuscules pour la couleur)
                    display_text = f"{word} ({color.upper()})"
                elif show_colors: # Mode triche/debug pour voir les couleurs cachées
                     color = self.color_matrix[r][c]
                     display_text = f"{word} [{color[:3].upper()}]" # Affiche mot et 3 premières lettres couleur
                else:
                    # Affiche juste le mot si non révélé
                    display_text = word
                # Ajuste la largeur de la cellule
                print(f"{display_text:<{col_width}}", end=" | ")
            print() # Nouvelle ligne à la fin de chaque rangée
        print("-" * (col_width * self.BOARD_SIZE + (self.BOARD_SIZE * 3))) # Ligne séparatrice
        print(f"Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")


    def play_turn(self):
        """Gère un tour complet pour le joueur actuel."""
        if self.game_over:
            print(f"\nLa partie est terminée. Le gagnant est l'équipe {self.winner.upper()} !")
            return False # Indique que le jeu ne continue pas

        print(f"\n=== Tour de l'équipe {self.current_player.upper()} ===")
        self.display_board() # Affiche le plateau avant le tour

        # 1. Obtenir l'indice de l'espion
        keyword, number = self.get_clue()
        print(f"\nL'équipe {self.current_player.upper()} doit deviner {number} mot(s) liés à '{keyword}'.")

        # 2. Phase de devinette (max number + 1 tentatives)
        guesses_left = number + 1
        for i in range(number + 1):
            print(f"\nTentative {i+1}/{number} (max {number+1} si correctes consécutivement).")
            guess_result = self.make_guess()

            if guess_result == 'WIN':
                print(f"\nFélicitations équipe {self.current_player.upper()}, vous avez gagné !")
                self.display_board(show_colors=True) # Montre tout à la fin
                return False # Jeu terminé
            elif guess_result == 'LOSS':
                 # Le message de défaite est déjà affiché dans make_guess
                 self.display_board(show_colors=True)
                 return False # Jeu terminé
            elif guess_result is False:
                # Mauvaise réponse (neutre, adversaire) ou 'PASSE'
                print("Fin du tour.")
                break # Sortir de la boucle de devinette
            # Si guess_result is True, la devinette était correcte, on continue

        # 3. Vérifier la victoire (si l'adversaire a gagné sur une mauvaise pioche)
        if not self.game_over and self._check_win_condition():
             print(f"\nL'équipe {self.winner.upper()} a gagné !")
             self.display_board(show_colors=True)
             return False # Jeu terminé

        # 4. Changer de joueur pour le prochain tour
        self._switch_player()
        return True # Indique que le jeu continue


# --- Exemple d'exécution ---
if __name__ == "__main__":
    game = Game()

    # Boucle de jeu simple
    turn_count = 1
    while not game.game_over:
        print(f"\n===== TOUR {turn_count} =====")
        if not game.play_turn():
            break # Sortir si play_turn retourne False (jeu terminé)
        turn_count += 1

    print("\nFin de la partie.")
    if game.winner:
        print(f"L'équipe {game.winner.upper()} a remporté la victoire !")
    else:
        # Normalement, ne devrait pas arriver sauf si interrompu
        print("La partie s'est terminée sans vainqueur désigné.")

