from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import uuid
from enum import Enum

app = FastAPI(title="Word Game API")

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

class Game(BaseModel):
    id: str
    cards: List[Card]
    current_turn: str  # "red" or "blue"
    current_clue: Optional[str] = None
    current_clue_number: Optional[int] = None
    red_cards_left: int
    blue_cards_left: int
    winner: Optional[str] = None

class CreateGameRequest(BaseModel):
    cards: List[Dict]
    game_id: Optional[str] = None

class CreateGameResponse(BaseModel):
    game_id: str
    first_player: str

class ClueRequest(BaseModel):
    game_id: str
    team_color: str

class ClueResponse(BaseModel):
    clue: str
    number: int

class GameStateRequest(BaseModel):
    game_id: str

class GameStateResponse(BaseModel):
    current_turn: str
    current_clue: Optional[str]
    current_clue_number: Optional[int]
    board: List[Card]
    red_cards_left: int
    blue_cards_left: int
    winner: Optional[str]

class GuessRequest(BaseModel):
    game_id: str
    word: str

class GuessResponse(BaseModel):
    correct: bool
    card_color: CardColor
    board: List[Card]
    game_over: bool
    winner: Optional[str]

# In-memory storage for games
games = {}

# Routes
@app.post("/game", response_model=CreateGameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game with the given cards and ID."""
    # This is a placeholder - in a real implementation, you would:
    # - Validate the cards
    # - Assign colors if not provided
    # - Determine the first player
    
    game_id = request.game_id or str(uuid.uuid4())
    
    if game_id in games:
        raise HTTPException(status_code=400, detail="Game ID already exists")
    
    # Convert dict to Card objects
    cards = [Card(**card) for card in request.cards]
    
    # Count cards by color for tracking
    red_count = sum(1 for card in cards if card.color == CardColor.RED)
    blue_count = sum(1 for card in cards if card.color == CardColor.BLUE)
    
    # Determine first player (placeholder logic)
    first_player = "red" if red_count > blue_count else "blue"
    
    # Create and store the game
    games[game_id] = Game(
        id=game_id,
        cards=cards,
        current_turn=first_player,
        red_cards_left=red_count,
        blue_cards_left=blue_count,
    )
    
    return CreateGameResponse(game_id=game_id, first_player=first_player)

@app.post("/clue", response_model=ClueResponse)
async def get_ai_clue(request: ClueRequest):
    """Get an AI-generated clue for the given team."""
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[request.game_id]
    
    # Placeholder for AI clue generation logic
    def generate_clue(game: Game, team_color: str) -> tuple:
        # In a real implementation, this would use an AI model to generate a relevant clue
        # based on the remaining cards of the team's color
        return "placeholder_clue", 2
    
    clue_word, clue_number = generate_clue(game, request.team_color)
    
    # Update game state
    game.current_clue = clue_word
    game.current_clue_number = clue_number
    
    return ClueResponse(clue=clue_word, number=clue_number)

@app.get("/game/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """Get the current state of the game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    return GameStateResponse(
        current_turn=game.current_turn,
        current_clue=game.current_clue,
        current_clue_number=game.current_clue_number,
        board=game.cards,
        red_cards_left=game.red_cards_left,
        blue_cards_left=game.blue_cards_left,
        winner=game.winner
    )

@app.post("/guess", response_model=GuessResponse)
async def make_guess(request: GuessRequest):
    """Submit a guess for a word."""
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[request.game_id]
    
    # Find the card with the guessed word
    found_card = None
    for card in game.cards:
        if card.word.lower() == request.word.lower():
            found_card = card
            break
    
    if not found_card:
        raise HTTPException(status_code=400, detail="Word not found on the board")
    
    if found_card.revealed:
        raise HTTPException(status_code=400, detail="Card already revealed")
    
    # Reveal the card
    found_card.revealed = True
    
    # Update game state based on the guess
    game_over = False
    correct_guess = found_card.color == CardColor(game.current_turn)
    
    # Update cards left count
    if found_card.color == CardColor.RED:
        game.red_cards_left -= 1
        if game.red_cards_left == 0:
            game.winner = "red"
            game_over = True
    elif found_card.color == CardColor.BLUE:
        game.blue_cards_left -= 1
        if game.blue_cards_left == 0:
            game.winner = "blue"
            game_over = True
    elif found_card.color == CardColor.ASSASSIN:
        game.winner = "blue" if game.current_turn == "red" else "red"
        game_over = True
    
    # Switch turns if guess was incorrect or if it was the assassin
    if not correct_guess or found_card.color == CardColor.ASSASSIN:
        game.current_turn = "blue" if game.current_turn == "red" else "red"
    
    return GuessResponse(
        correct=correct_guess,
        card_color=found_card.color,
        board=game.cards,
        game_over=game_over,
        winner=game.winner
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)