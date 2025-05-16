<template>
  <div v-if="isLoading" class="loading">Loading game data...</div>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  <div v-if="!isLoading && gameData" class="game-container">
    <!-- Desktop layout -->
    <div class="desktop-layout">
      <div v-if="gameData.winner" class="winner-announcement">
        <h2>Game Over! {{ gameData.winner.toUpperCase() }} team wins!</h2>
        <button @click="goToCreatePage">Play Again</button>
      </div>
      <div class="top-panels">
        <ClueDisplay
          :currentClue="gameData.current_clue"
          :currentClueNumber="gameData.current_clue_number"
          :guessesCorrectThisRound="gameData.guesses_correct_this_round"
          :currentPLayer="gameData.current_player"
        />
        <ScoreBoard
          :redScore="gameData.red_score"
          :blueScore="gameData.blue_score"
          :userMessage="userMessage"
        />
      </div>

      <GameBoard
        :wordMatrix="gameData.word_matrix"
        :colorMatrix="gameData.color_matrix"
        :revealedMatrix="gameData.revealed_matrix"
        :isGameOver="!!gameData.winner"
        @card-clicked="handleCardGuess"
      />

      <button
        class="pass-button desktop-pass"
        @click="handleCardGuess('PASSE')"
      >
        Pass
      </button>
    </div>

    <!-- Mobile landscape layout - Only displays in landscape mode on mobile -->
    <div class="mobile-landscape-layout">
      <!-- Left column for mobile landscape mode -->
      <div class="left-column">
        <ClueDisplay
          :currentClue="gameData.current_clue"
          :currentClueNumber="gameData.current_clue_number"
          :guessesCorrectThisRound="gameData.guesses_correct_this_round"
          :currentPLayer="gameData.current_player"
          class="clue-display"
        />
        <ScoreBoard
          :redScore="gameData.red_score"
          :blueScore="gameData.blue_score"
          :userMessage="userMessage"
          class="score-board"
        />
      </div>

      <!-- Right column - game board -->
      <div class="right-column">
        <GameBoard
          :wordMatrix="gameData.word_matrix"
          :colorMatrix="gameData.color_matrix"
          :revealedMatrix="gameData.revealed_matrix"
          :isGameOver="!!gameData.winner"
          @card-clicked="handleCardGuess"
          class="game-board"
        />
        <button class="pass-button" @click="handleCardGuess('PASSE')">
          Pass
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import ClueDisplay from "../components/ClueDisplay.vue";
import ScoreBoard from "../components/ScoreBoard.vue";
import GameBoard from "../components/GameBoard.vue";

const props = defineProps({
  gameId: {
    type: String,
    required: true,
  },
});

const route = useRoute();
const router = useRouter();
const gameData = ref(null);
const isLoading = ref(true);
const errorMessage = ref("");
const userMessage = ref("Game started. Waiting for the first clue."); // Initial message

async function fetchGameData() {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const response = await axios.get(`/game/${props.gameId}`);
    gameData.value = response.data;
    console.log(gameData);

    // The GET /game/{game_id} response doesn't include the 'userMassage' from the /guess endpoint.
    // We'll update userMessage primarily after a guess.
    // You might want to add a general 'current turn' message here if available from gameData.
    if (gameData.value && gameData.value.current_turn) {
      userMessage.value = `It's ${gameData.value.current_turn}'s turn.`;
    } else if (gameData.value && gameData.value.winner) {
      userMessage.value = `Game Over! ${gameData.value.winner.toUpperCase()} team wins!`;
    }
  } catch (error) {
    console.error("Error fetching game data:", error);
    if (error.response && error.response.status === 404) {
      errorMessage.value = `Game with ID ${props.gameId} not found.`;
    } else if (
      error.response &&
      error.response.data &&
      error.response.data.detail
    ) {
      errorMessage.value = `Error: ${error.response.data.detail}`;
    } else {
      errorMessage.value = "Failed to load game data. Please try refreshing.";
    }
    gameData.value = null; // Clear stale data
  } finally {
    isLoading.value = false;
  }
}

async function handleCardGuess(word) {
  if (gameData.value && gameData.value.winner) {
    userMessage.value = "The game is over.";
    return;
  }
  isLoading.value = true; // Indicate activity
  errorMessage.value = ""; // Clear previous errors

  try {
    const response = await axios.post("/guess", {
      game_id: props.gameId,
      guess_word: word,
    });
    // The 'userMassage' is key here for feedback.
    if (response.data && response.data.userMassage) {
      userMessage.value = response.data.userMassage.replace(/\n/g, " "); // Replace newlines for better display
    } else {
      userMessage.value = `Guess for '${word}' processed.`;
    }

    // After a guess, always refresh the entire game state
    await fetchGameData();
  } catch (error) {
    console.error("Error making guess:", error);
    if (error.response && error.response.data && error.response.data.detail) {
      if (Array.isArray(error.response.data.detail)) {
        errorMessage.value = error.response.data.detail
          .map((d) => `${d.loc.join("->")}: ${d.msg}`)
          .join(", ");
      } else {
        errorMessage.value = `Guess Error: ${error.response.data.detail}`;
      }
      userMessage.value = `Failed to process guess for '${word}'.`;
    } else {
      errorMessage.value = "An unexpected error occurred while making a guess.";
      userMessage.value = `Failed to process guess for '${word}'.`;
    }
    isLoading.value = false; // Ensure loading is set to false on error if not refetching
  }
  // fetchGameData sets isLoading to false at its end.
}

function goToCreatePage() {
  router.push({ name: "CreateGame" });
}

onMounted(() => {
  fetchGameData();
});

// Optional: Watch for changes in gameId if the component could be reused for different games without full remount
watch(
  () => props.gameId,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      fetchGameData();
    }
  }
);
</script>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: anchor-center;
  gap: 20px;
  /* padding: 20px; */
  width: 100%;
}

/* Desktop layout styling */
.desktop-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.top-panels {
  display: flex;
  justify-content: space-around;
  width: 100%;
  max-width: 900px;
  gap: 20px;
  margin-bottom: 20px;
}

.desktop-pass {
  margin-top: 10px;
}

/* Mobile landscape layout styling - Hidden by default */
.mobile-landscape-layout {
  display: none;
  width: 100%;
  max-width: 1200px;
}

.pass-button {
  background-color: #e1b475;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.pass-button:hover {
  background-color: #d0a365;
}

.winner-announcement {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #dff0d8;
  color: #3c763d;
  border: 1px solid #d6e9c6;
  border-radius: 8px;
  text-align: center;
  width: 100%;
  max-width: 900px;
}

.winner-announcement button {
  margin-top: 10px;
  background-color: #5cb85c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.winner-announcement button:hover {
  background-color: #4cae4c;
}

/* Mobile landscape mode specific layout */
@media screen and (orientation: landscape) and (max-width: 1024px) {
  /* Hide desktop layout on mobile landscape */
  .desktop-layout {
    display: none;
  }

  /* Show mobile landscape layout */
  .mobile-landscape-layout {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    gap: 20px;
  }

  .left-column {
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Items will stack from top with no extra spacing */
    gap: 8px; /* Optional: consistent small space between items */
  }

  .right-column {
    width: 70%;
    display: flex;
    flex-direction: column; /* Disposition en colonne */
    align-items: flex-end; /* Aligné à gauche */
    justify-content: flex-start; /* En haut (optionnel) */
    margin-right: 20px;
  }

  .clue-display {
    margin-bottom: 0;
  }

  .score-board {
    margin: 0;
  }

  .pass-button {
    margin-top: 10px;
  }

  .game-board {
    width: 90%;
    height: 50%;
  }
}

/* Additional media query for very small screens */
@media screen and (orientation: landscape) and (max-height: 500px) {
  .mobile-landscape-layout {
    padding: 10px;
  }

  .left-column {
    width: 35%;
  }

  .right-column {
    width: 65%;
  }
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: #a94442;
  background-color: #f2dede;
  border: 1px solid #ebccd1;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  text-align: center;
  width: 100%;
  max-width: 900px;
}

@media screen and (orientation: landscape) and (max-width: 1024px) {
  .winner-announcement {
    position: absolute;
    top: 10%;
    left: 5%;
    z-index: 1000;
    background-color: rgba(223, 240, 216, 0.9); /* Slight transparency */
    color: #3c763d;
    border: 1px solid #d6e9c6;
    border-radius: 8px;
    text-align: center;
    padding: 16px;
    width: 90%;
    max-width: 320px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
}
</style>
