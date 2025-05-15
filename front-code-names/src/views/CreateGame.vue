<template>
  <div class="create-game-container">
    <h1>Create Codenames Game</h1>
    <!-- <div class="words-input-grid">
      <div v-for="(word, index) in words" :key="index" class="word-input-item">
        <label :for="'word-' + index">Word {{ index + 1 }}</label>
        <input type="text" v-model="words[index]" :id="'word-' + index" />
      </div>
    </div> -->
    <button @click="handleCreateGame" :disabled="isLoading">
      {{ isLoading ? "Creating..." : "Launch Game" }}
    </button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const defaultWords = [
  "Hollywood",
  "Screen",
  "Play",
  "Marble",
  "Dinosaur",
  "Cat",
  "Telescope",
  "Nurse",
  "Mail",
  "Fly",
  "Atlantis",
  "Trick",
  "Watch",
  "Space",
  "Flute",
  "Carrot",
  "Robin",
  "Shakespeare",
  "Collar",
  "Web",
  "Desk",
  "Unicorn",
  "Match",
  "Sub",
  "Time",
];
const words = ref([...defaultWords]); // Initialize with default words
const isLoading = ref(false);
const errorMessage = ref("");

async function handleCreateGame() {
  isLoading.value = true;
  errorMessage.value = "";
  const gameWords = words.value.filter((word) => word.trim() !== ""); // Filter out empty strings

  if (gameWords.length !== 25) {
    errorMessage.value = "Please provide exactly 25 words.";
    isLoading.value = false;
    return;
  }

  try {
    const response = await axios.post("/game", { cards: gameWords });
    if (response.data && response.data.game_id) {
      // Navigate to the game view with the game ID
      router.push({
        name: "GameView",
        params: { gameId: response.data.game_id },
      });
    } else {
      errorMessage.value = "Failed to create game: No game ID received.";
    }
  } catch (error) {
    console.error("Error creating game:", error);
    if (error.response && error.response.data && error.response.data.detail) {
      if (Array.isArray(error.response.data.detail)) {
        errorMessage.value = error.response.data.detail
          .map((d) => `${d.loc.join("->")}: ${d.msg}`)
          .join(", ");
      } else {
        errorMessage.value = `Error: ${error.response.data.detail}`;
      }
    } else {
      errorMessage.value =
        "An unexpected error occurred while creating the game.";
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.create-game-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.words-input-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.word-input-item {
  display: flex;
  flex-direction: column;
}

.word-input-item label {
  font-size: 0.8em;
  margin-bottom: 3px;
  color: #555;
}

.word-input-item input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9em;
}

button {
  background-color: #5cb85c;
  color: white;
  padding: 12px 25px;
}

button:hover {
  background-color: #4cae4c;
}
</style>
