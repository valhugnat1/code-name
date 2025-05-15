<template>
  <div class="clue-display-module">
    <h4>Clue Information</h4>
    <div
      v-if="
        currentClue !== null && currentClue !== undefined && currentClue !== ''
      "
    >
      <p><strong>Clue:</strong> {{ currentClue }}</p>
      <p><strong>Number:</strong> {{ currentClueNumber }}</p>
      <p>
        <strong>Guesses Remaining:</strong>
        {{ guessesLeft >= 0 ? guessesLeft : "N/A" }}
      </p>
      <p>
        <strong>Current player: </strong>
        <span :class="playerColorClass">{{ currentPLayer }}</span>
      </p>
    </div>
    <div v-else>
      <p>Waiting for the Spymaster's clue...</p>
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";
const props = defineProps({
  currentClue: String,
  currentClueNumber: Number,
  guessesCorrectThisRound: {
    // From backend: guesses_correct_this_round
    type: Number,
    default: 0,
  },
  currentPLayer: String,
});
const guessesLeft = computed(() => {
  if (props.currentClueNumber === null || props.currentClueNumber === undefined)
    return "N/A";
  // The clue number indicates total allowed guesses for the clue.
  // Guesses left would be ClueNumber - GuessesMadeThisTurnForThisClue
  // The backend provides `guesses_correct_this_round` which seems to track successful guesses within the current clue's scope.
  return props.currentClueNumber - props.guessesCorrectThisRound;
});

const playerColorClass = computed(() => {
  // Assuming the currentPLayer string contains the team name/color (e.g., "Blue Team" or "Red Team")
  if (!props.currentPLayer) return "";

  const playerLower = props.currentPLayer.toLowerCase();
  if (playerLower.includes("red")) {
    return "red-player";
  } else if (playerLower.includes("blue")) {
    return "blue-player";
  }
  return "";
});
</script>
<style scoped>
.clue-display-module {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 200px;
  text-align: left;
}
.clue-display-module h4 {
  margin-top: 0;
  color: #337ab7;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}
.clue-display-module p {
  margin: 8px 0;
  font-size: 0.95em;
}
.clue-display-module strong {
  color: #555;
}
.red-player {
  color: #d9534f;
  font-weight: bold;
  text-transform: capitalize;
}
.blue-player {
  color: #337ab7;
  font-weight: bold;
  text-transform: capitalize;
}
</style>
