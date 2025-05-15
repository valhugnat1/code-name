// src/services/api.js
import axios from "axios";

const API_URL = "http://localhost:8000"; // Your backend URL

export default {
  createGame(cards) {
    return axios.post(`${API_URL}/game`, { cards });
  },
  getGameState(gameId) {
    return axios.get(`${API_URL}/game/${gameId}`);
  },
  makeGuess(gameId, guessWord) {
    return axios.post(`${API_URL}/guess`, {
      game_id: gameId,
      guess_word: guessWord,
    });
  },
};
