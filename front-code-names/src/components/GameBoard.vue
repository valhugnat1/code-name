<template>
  <div class="game-board-grid">
    <template v-for="(row, rowIndex) in wordMatrix" :key="`row-${rowIndex}`">
      <GameCard
        v-for="(word, colIndex) in row"
        :key="`card-${rowIndex}-${colIndex}`"
        :word="word"
        :isRevealed="revealedMatrix[rowIndex][colIndex]"
        :color="
          revealedMatrix[rowIndex][colIndex]
            ? colorMatrix[rowIndex][colIndex]
            : 'hidden'
        "
        :isDisabled="isGameOver || revealedMatrix[rowIndex][colIndex]"
        @click="onCardClick(word, rowIndex, colIndex)"
      />
    </template>
  </div>
</template>

<script setup>
import GameCard from "./GameCard.vue";

const props = defineProps({
  wordMatrix: Array, // 5x5 array of words
  colorMatrix: Array, // 5x5 array of colors ('red', 'blue', 'neutral', 'assassin')
  revealedMatrix: Array, // 5x5 array of booleans
  isGameOver: Boolean,
});

const emit = defineEmits(["card-clicked"]);

function onCardClick(word, rowIndex, colIndex) {
  if (!props.revealedMatrix[rowIndex][colIndex] && !props.isGameOver) {
    emit("card-clicked", word);
  }
}
</script>

<style scoped>
.game-board-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr); /* Ensure square cells if desired */
  gap: 10px;
  padding: 15px;
  background-color: #e9e9e9;
  border-radius: 8px;
  width: 100%;
  max-width: 600px; /* Adjust for desired board size */
  aspect-ratio: 1 / 1; /* Make the board square */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
