from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
import json
import os
from enum import Enum
from game_saving import Game

app = FastAPI(title="Word Game API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify exact origins: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Ensure games directory exists
GAMES_DIR = "games"
os.makedirs(GAMES_DIR, exist_ok=True)

# Models
class CardColor(str, Enum):
    RED = "red"
    BLUE = "blue"
    NEUTRAL = "neutral"
    ASSASSIN = "assassin"

class Card(BaseModel):
    word: str
    color: CardColor
    revealed: bool = False

class CreateGameRequest(BaseModel):
    cards: List[str]

class CreateGameResponse(BaseModel):
    game_id: str
    first_player: str

class ClueRequest(BaseModel):
    game_id: str
    team_color: str

class ClueResponse(BaseModel):
    clue: str
    number: int

class GameStateResponse(BaseModel):
    current_clue: Optional[str]
    current_clue_number: Optional[int]
    red_score: int
    blue_score: int
    guesses_correct_this_round: int
    winner: Optional[str]
    color_matrix: List[List[str]]
    word_matrix: List[List[str]]
    revealed_matrix: List[List[bool]]

class GuessRequest(BaseModel):
    game_id: str
    guess_word: str

class GuessResponse(BaseModel):
    guess_status: str
    game_over: bool
    userMassage: str
    winner: Optional[str]


# File operations for game storage
def save_game(game):
    """Save game to a JSON file"""
    filename_save = os.path.join(GAMES_DIR, f"{game.id_game}.json")
    
    with open(filename_save, 'w', encoding='utf-8') as f:
        f.write(game.to_json_string())


def load_game(game_id: str):
    """Load game from a JSON file"""
    file_path = os.path.join(GAMES_DIR, f"{game_id}.json")
    print (file_path)
    
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = f.read()

        print (json_data)
        game = Game.from_json_string(json_data)
        print(f"Partie chargée depuis '{file_path}'.")
        return game
    except FileNotFoundError:
        print(f"Erreur : Fichier '{file_path}' non trouvé.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier '{file_path}' ne contient pas de JSON valide.")
    # except Exception as e:
    #     print(f"Erreur inattendue lors du chargement de la partie : {e}")
        # Optionnellement, demander à nouveau ou commencer une nouvelle partie

# Routes
@app.post("/game", response_model=CreateGameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game with the given cards and ID."""
    game = Game()
    # Check if game already exists
    if os.path.exists(os.path.join(GAMES_DIR, f"{game.id_game}.json")):
        raise HTTPException(status_code=400, detail="Game ID already exists")

    game.turn_display_counter = 1 
    game.get_clue()
    game.guesses_correct_this_round = 0

    # Save game to file
    save_game(game)
    
    return CreateGameResponse(game_id=game.id_game, first_player=game.current_player)

@app.get("/game/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """Get the current state of the game."""
    print (game_id)
    game = load_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    keyword = game.keyword
    max_guesses_this_round = game.number_gess_given + 1 if game.number_gess_given > 0 else 1
    attempt_num = game.guesses_correct_this_round + 1

    game.display_board(show_colors=True)


    print(f"\nDevinette {attempt_num}/{max_guesses_this_round} pour l'indice '{keyword}, {game.number_gess_given}'.")
    
    return GameStateResponse(
        current_clue=game.keyword,
        current_clue_number=game.number_gess_given,
        red_score=game.red_score,
        blue_score=game.blue_score,
        guesses_correct_this_round=game.guesses_correct_this_round,
        current_player=game.current_player,
        winner=game.winner,
        color_matrix=game.color_matrix,
        word_matrix=game.word_matrix,
        revealed_matrix=game.revealed_matrix
    )

@app.post("/guess", response_model=GuessResponse)
async def make_guess(request: GuessRequest):
    """Submit a guess for a word."""
    game = load_game(request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    response = GuessResponse(
        guess_status="",
        game_over=False,
        userMassage="",
        winner="",
    )

    max_guesses_this_round = game.number_gess_given + 1 if game.number_gess_given > 0 else 1
    attempt_num = game.guesses_correct_this_round + 1

    
    # Si toutes les cibles de l'indice ont été trouvées et qu'il reste des tentatives (le +1)
    if game.number_gess_given > 0 and game.guesses_correct_this_round == game.number_gess_given and attempt_num > game.number_gess_given:
            print("Vous avez trouvé tous les mots de l'indice. Ceci est une devinette bonus.")
    elif game.number_gess_given == 0 and attempt_num ==1:
            print("Indice '0'. Vous pouvez tenter une devinette ou passer.")
    

    guess_word_input = request.guess_word.strip().upper()

    if guess_word_input == 'PASSE':
        print("L'équipe passe son tour.")
        game.end_round()
        response.userMassage += "L'équipe passe son tour.\n"
        
    else : 
        guess_status, messageUser = game.process_guess(guess_word_input)
        response.userMassage += messageUser + "\n"

        if guess_status == 'INVALID_WORD':
            print(f"Le mot '{guess_word_input}' n'est pas sur le plateau. Réessayez cette tentative.")
            raise HTTPException(status_code=500, detail="Invalid word")
        elif guess_status == 'ALREADY_REVEALED':
            print(f"Le mot '{guess_word_input}' a déjà été révélé.")
            raise HTTPException(status_code=500, detail="Already revealed")
        
        elif guess_status == 'NEUTRAL' or guess_status == 'OPPONENT' or guess_status == 'ASSASSIN_LOSS':
            response.userMassage += "Fin du tour pour cette équipe.\n"
            print("Fin du tour pour cette équipe.")
            game.end_round()

        elif guess_status == 'CORRECT_CONTINUE':
            game.guesses_correct_this_round += 1
            if game.number_gess_given > 0 and game.guesses_correct_this_round == game.number_gess_given:
                response.userMassage += f"Vous avez trouvé les {game.number_gess_given} mots cibles de l'indice !\n"
                print(f"Vous avez trouvé les {game.number_gess_given} mots cibles de l'indice !")

                if attempt_num < max_guesses_this_round:
                    response.userMassage += "Vous avez encore une devinette bonus si vous le souhaitez.\n"
                    print("Vous avez encore une devinette bonus si vous le souhaitez.")
                # Si attempt_num == max_guesses_this_round, la boucle se terminera naturellement.
            elif game.number_gess_given == 0 and guess_status == 'CORRECT_CONTINUE': # Trouvé un mot correct sur un indice 0
                response.userMassage += "Fin du tour pour cette équipe (indice 0 et mot correct trouvé).\n"
                print("Fin du tour pour cette équipe (indice 0 et mot correct trouvé).")
                game.end_round()
    # Save updated game
    save_game(game)

    if game.game_over: # L'adversaire a pu gagner
        print(f"L'équipe {game.winner.upper()} a gagné !")
        response.userMassage += f"L'équipe {game.winner.upper()} a gagné !\n"
        response.game_over = True
        response.winner = game.winner.upper()

    game.display_board(show_colors=True)
    
    return response

if __name__ == "__main__":
    uvicorn.run("api_codename:app", host="0.0.0.0", port=8000, reload=True)