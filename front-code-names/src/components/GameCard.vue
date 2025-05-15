<template>
  <button
    class="card"
    :class="[cardColorClass, { revealed: isRevealed, disabled: isDisabled }]"
    :disabled="isDisabled"
  >
    {{ word }}
  </button>
</template>
<script setup>
import { computed } from "vue";
const props = defineProps({
  word: String,
  isRevealed: Boolean,
  color: String, // 'red', 'blue', 'neutral', 'assassin', or 'hidden'
  isDisabled: Boolean,
});
const cardColorClass = computed(() => {
  if (!props.isRevealed) {
    return "card-hidden";
  }
  switch (props.color) {
    case "red":
      return "card-red";
    case "blue":
      return "card-blue";
    case "neutral":
      return "card-neutral";
    case "assassin":
      return "card-assassin";
    default:
      return "card-hidden"; // Fallback, though should be one of the above if revealed
  }
});
</script>
<style scoped>
.card {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%; /* Fill cell from grid */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1em; /* Adjust based on card size */
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  overflow-wrap: break-word; /* Prevent long words from breaking layout badly */
  word-break: break-word;
  text-align: center;
  background-color: #fff; /* Default for hidden */
  color: #333;
}
.card:not(.revealed):not(.disabled):hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}
.card.revealed {
  cursor: default;
  color: white; /* Default text color for revealed cards */
}
.card.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
.card.disabled:not(.revealed) {
  /* Keep unrevealed disabled cards looking like hidden cards */
  background-color: #fff;
  color: #aaa;
}
.card.disabled:hover {
  transform: none;
}
.card-hidden {
  background-color: #ffffff;
  color: #333333;
  border: 2px dashed #bbbbbb;
}
.card-red {
  background-color: #d9534f; /* Bootstrap danger */
}
.card-blue {
  background-color: #0275d8; /* Bootstrap primary */
}
.card-neutral {
  background-color: #f0ad4e; /* Bootstrap warning - for neutral agents */
  color: #333; /* Darker text for better contrast on yellow */
}
.card-assassin {
  background-color: #292b2c; /* Bootstrap inverse/dark */
}

/* Landscape mode specific styling for cards */
@media screen and (orientation: landscape) and (max-width: 1024px) {
  .card {
    padding: 5px;
    font-size: 0.8em; /* Reduce font size */
    margin: auto; /* Center the card within its cell */
  }

  /* Adjust hover effect for smaller cards */
  .card:not(.revealed):not(.disabled):hover {
    transform: translateY(-1px);
  }
}

/* Further adjustments for very small screens */
@media screen and (orientation: landscape) and (max-height: 500px) {
  .card {
    font-size: 0.7em;
    padding: 3px;
  }
}
</style>
