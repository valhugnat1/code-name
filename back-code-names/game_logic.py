import random
import json
import uuid # Ajout de l'import pour la sérialisation JSON

from dotenv import load_dotenv
import os

# Pour utiliser l'API OpenAI, vous devez l'installer : pip install openai
# et configurer votre clé API (par exemple via une variable d'environnement OPENAI_API_KEY)
# import openai
from openai import OpenAI # Utilisation recommandée pour les versions récentes

class Game:
    """
    Représente une partie du jeu de type Codenames.
    Gère le plateau de jeu, les tours des joueurs, les devinettes et la condition de victoire.
    Permet la sauvegarde et le chargement de l'état du jeu via JSON.
    """
    BOARD_SIZE = 5

    def __init__(self, game_words=None, load_data=None):
        """
        Initialise une nouvelle partie ou charge une partie depuis des données.
        Args:
            load_data (dict, optional): Dictionnaire contenant l'état du jeu à charger.
                                        Si None, une nouvelle partie est initialisée.
        """
        if load_data:
            self._load_state_from_data(load_data)
        else:
            self._initialize_new_game_state(game_words)

    def _initialize_new_game_state(self, game_words):
        """Initialise l'état pour une nouvelle partie."""
        print("Initialisation d'une nouvelle partie...")
        self.id_game = str(uuid.uuid4()) 
        
        # Initialisation des matrices vides
        self.color_matrix = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.word_matrix = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.revealed_matrix = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        # Scores des équipes
        self.red_score = 0
        self.blue_score = 0

        self.keyword = ""
        self.number_gess_given = 0
        self.guesses_correct_this_round = 0
        self.turn_display_counter = 0


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

        # Initialisation des matrices de mots et couleurs (avec placeholders pour votre code)
        self._initialize_color_matrix()
        self._initialize_word_matrix(game_words)

        print(f"Objectif : {self.red_cards_total} cartes pour ROUGE, {self.blue_cards_total} cartes pour BLEU.")

        self.game_over = False
        self.winner = None
        # self.turn_count = 1 # Optionnel: si vous voulez sauvegarder le numéro du tour

    def _load_state_from_data(self, data):
        """Charge l'état du jeu à partir d'un dictionnaire de données."""
        print("Chargement de l'état du jeu depuis les données...")
        # Vérification optionnelle de la taille du plateau
        loaded_board_size = data.get('board_size', self.BOARD_SIZE)
        if loaded_board_size != self.BOARD_SIZE:
            raise ValueError(
                f"Taille de plateau incompatible ({loaded_board_size}) dans les données sauvegardées. "
                f"Attendu : {self.BOARD_SIZE}"
            )

        self.id_game = data['id_game']
        self.color_matrix = data['color_matrix']
        self.word_matrix = data['word_matrix']
        self.revealed_matrix = data['revealed_matrix']
        self.red_score = data['red_score']
        self.blue_score = data['blue_score']
        self.current_player = data['current_player']
        self.red_cards_total = data['red_cards_total']
        self.blue_cards_total = data['blue_cards_total']
        self.game_over = data['game_over']
        self.winner = data['winner']
        self.keyword = data['keyword']
        self.number_gess_given = data['number_gess_given']
        self.guesses_correct_this_round = data['guesses_correct_this_round']
        self.turn_display_counter = data['turn_display_counter']

        # self.turn_count = data.get('turn_count', 1) # Charger le numéro du tour
        print("État du jeu chargé.")

    @classmethod
    def from_json_string(cls, json_str):
        """Crée une instance de Game à partir d'une chaîne JSON."""
        data = json.loads(json_str)
        return cls(load_data=data)

    def to_json_string(self):
        """Sérialise l'état actuel du jeu en une chaîne JSON."""
        state = {
            'id_game': self.id_game,
            'board_size': self.BOARD_SIZE,
            'color_matrix': self.color_matrix,
            'word_matrix': self.word_matrix,
            'revealed_matrix': self.revealed_matrix,
            'red_score': self.red_score,
            'blue_score': self.blue_score,
            'current_player': self.current_player,
            'red_cards_total': self.red_cards_total,
            'blue_cards_total': self.blue_cards_total,
            'game_over': self.game_over,
            'winner': self.winner,
            'keyword': self.keyword,
            'number_gess_given': self.number_gess_given,
            'guesses_correct_this_round': self.guesses_correct_this_round,
            'turn_display_counter': self.turn_display_counter

            # 'turn_count': self.turn_count, # Si vous suivez le numéro du tour dans self
        }
        return json.dumps(state, indent=2) # indent=2 pour une sortie JSON lisible

    def _initialize_color_matrix(self):
        """
        Méthode pour initialiser la matrice des couleurs.
        !!! REMPLACEZ CE CODE PAR VOTRE LOGIQUE D'INITIALISATION !!!
        """
        print("Initialisation de la matrice des couleurs (placeholder)...")
        colors = ['red'] * self.red_cards_total + \
                 ['blue'] * self.blue_cards_total + \
                 ['assassin'] * 1
        neutral_count = self.BOARD_SIZE * self.BOARD_SIZE - len(colors)
        colors += ['neutral'] * neutral_count
        random.shuffle(colors)

        k = 0
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                self.color_matrix[r][c] = colors[k]
                k += 1
        print("Matrice des couleurs initialisée.")

    def _initialize_word_matrix(self, game_words):
        """
        Méthode pour initialiser la matrice des mots.
        !!! REMPLACEZ CE CODE PAR VOTRE LOGIQUE D'INITIALISATION !!!
        """
        print("Initialisation de la matrice des mots (placeholder)...")
        # words = [
        #     "LUNE", "CHEVAL", "PIRATE", "MIROIR", "CHOCOLAT",
        #     "ROBOT", "PLAGE", "VAMPIRE", "TOUR", "FEU",
        #     "AVION", "BANANE", "NEIGE", "BANQUIER", "DRAGON",
        #     "SOURIS", "BIBLIOTHÈQUE", "COEUR", "NUAGE", "TRAIN",
        #     "FUSÉE", "TÉLÉPHONE", "MAGIE", "SOLDAT", "FORÊT"
        # ]
        # random.shuffle(words)
        k = 0
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                self.word_matrix[r][c] = game_words[k]
                k += 1
        print("Matrice des mots initialisée.")

    def _get_remaining_words(self, color):
        """Retourne la liste des mots non découverts pour une couleur donnée."""
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
        Obtient un indice (mot-clé et nombre) pour le joueur actuel (espion).
        """

        target_words = self._get_remaining_words(self.current_player)
        all_unrevealed_words = self._get_all_unrevealed_words()


        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("Clé API OpenAI non trouvée dans les variables d'environnement.")
            client = OpenAI(api_key=api_key)
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
            parts = clue_text.split(',')
            if len(parts) == 2:
                keyword = parts[0].strip().upper()
                try:
                    number = int(parts[1].strip())
                    if keyword not in all_unrevealed_words: # Vérification supplémentaire
                         print(f"Indice reçu de l'IA : {keyword}, {number}")
                         self.keyword = keyword
                         self.number_gess_given = number
                         return keyword, number
                    else:
                         print("Erreur : L'IA a donné un mot présent sur le plateau.")
                except ValueError:
                    print("Erreur : L'IA n'a pas retourné un chiffre valide.")
            else:
                 print("Erreur : Format de réponse inattendu de l'IA.")
            return keyword, number
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API OpenAI : {e}")
            print("Passage à la saisie manuelle de l'indice.")

    def _find_word_coords(self, word_guess):
        """Trouve les coordonnées (ligne, colonne) d'un mot dans word_matrix."""
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if self.word_matrix[r][c].upper() == word_guess.upper():
                    return r, c
        return None

    def process_guess(self, guessed_word):
        """
        Traite un mot deviné par l'équipe.
        Met à jour l'état du jeu (matrices, scores, game_over, winner).
        Retourne un statut indiquant le résultat de la devinette.
        Statuts possibles:
            'CORRECT_CONTINUE': Bonne pioche, l'équipe continue.
            'CORRECT_WIN': Bonne pioche, l'équipe gagne.
            'NEUTRAL': Pioche neutre, fin du tour de l'équipe.
            'OPPONENT': Pioche adverse, fin du tour de l'équipe. (Peut entraîner une victoire adverse)
            'ASSASSIN_LOSS': Pioche assassin, l'équipe perd immédiatement.
            'INVALID_WORD': Le mot n'est pas sur le plateau.
            'ALREADY_REVEALED': Le mot a déjà été révélé.
        """
        messageUser = ""
        coords = self._find_word_coords(guessed_word)

        if coords is None:
            return 'INVALID_WORD', messageUser

        r, c = coords
        if self.revealed_matrix[r][c]:
            return 'ALREADY_REVEALED', messageUser

        # Révéler la carte
        self.revealed_matrix[r][c] = True
        revealed_color = self.color_matrix[r][c]
        original_word = self.word_matrix[r][c]
        print(f" -> '{original_word}' est de couleur : {revealed_color.upper()}")
        messageUser = f" -> '{original_word}' est de couleur : {revealed_color.upper()}"

        if revealed_color == self.current_player:
            if self.current_player == 'red':
                self.red_score += 1
            else: # blue
                self.blue_score += 1
            print(f"Correct ! Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")
            if self._check_win_condition(): # Vérifie si cette pioche fait gagner
                return 'CORRECT_WIN', messageUser + f"l'equipe {self.winner} a gagné !"
            return 'CORRECT_CONTINUE', messageUser

        elif revealed_color == 'neutral':
            print("C'est une carte neutre.")
            return 'NEUTRAL', messageUser

        elif revealed_color == 'assassin':
            print("Oh non ! C'est l'assassin !")
            self.game_over = True
            self.winner = 'red' if self.current_player == 'blue' else 'blue' # L'autre équipe gagne
            print(f"L'équipe {self.winner.upper()} gagne !")
            return 'ASSASSIN_LOSS', messageUser

        else: # C'est une carte de l'adversaire
            opponent_actual_color = revealed_color # 'red' ou 'blue'
            if opponent_actual_color == 'red':
                self.red_score += 1
            else: # blue
                self.blue_score += 1
            print(f"C'est une carte de l'équipe {opponent_actual_color.upper()} ! Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")
            if self._check_win_condition(): # Vérifie si l'adversaire gagne grâce à cette pioche
                # self.game_over et self.winner sont mis à jour par _check_win_condition
                pass # La condition de victoire est gérée, le statut 'OPPONENT' indique fin de tour
            return 'OPPONENT', messageUser

    def _check_win_condition(self):
        """Vérifie si une condition de victoire est atteinte et met à jour game_over/winner."""
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

    def end_round(self):
        """Change le joueur actuel."""
        self._switch_player()
        self.keyword = ""
        self.number_gess_given = 0
        self.guesses_correct_this_round = 0

        self.get_clue()

    def display_board(self, show_colors=False):
        """Affiche le plateau de jeu dans la console."""
        print("\n--- PLATEAU DE JEU ---")
        col_width = 18  # Augmenté pour plus d'espace
        for r in range(self.BOARD_SIZE):
            row_str = []
            for c in range(self.BOARD_SIZE):
                word = self.word_matrix[r][c]
                if self.revealed_matrix[r][c]:
                    color = self.color_matrix[r][c]
                    display_text = f"{word} ({color.upper()})"
                elif show_colors: # Mode triche/debug
                    color = self.color_matrix[r][c]
                    display_text = f"{word} [{color[:4].upper()}]"
                else:
                    display_text = word
                row_str.append(f"{display_text:<{col_width}}")
            print(" | ".join(row_str))
            if r < self.BOARD_SIZE - 1:
                 print("-" * (col_width * self.BOARD_SIZE + (self.BOARD_SIZE -1) * 3)) # Ligne séparatrice
        print("=" * (col_width * self.BOARD_SIZE + (self.BOARD_SIZE-1) * 3)) # Ligne finale
        print(f"Score : ROUGE {self.red_score}/{self.red_cards_total} - BLEU {self.blue_score}/{self.blue_cards_total}")
