<template>
  <div class="score-board-module">
    <h4>Game Status</h4>
    <div class="scores">
      <span class="score red">Red: {{ redScore }}</span>
      <span class="score blue">Blue: {{ blueScore }}</span>
    </div>
    <div class="user-message-box">
      <p><strong>Message:</strong> {{ userMessageToDisplay }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({
  redScore: Number,
  blueScore: Number,
  userMessage: String, // This comes from GameView after a guess or on load
});

const userMessageToDisplay = computed(() => {
  return props.userMessage || "Waiting for action...";
});
</script>

<style scoped>
.score-board-module {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 300px;
  text-align: left;
}
.score-board-module h4 {
  margin-top: 0;
  color: #337ab7;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}
.scores {
  display: flex;
  justify-content: space-between;
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}
.score.red {
  color: #d9534f;
}
.score.blue {
  color: #0275d8;
}
.user-message-box {
  margin-top: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 4px;
  font-size: 0.9em;
  min-height: 40px; /* To avoid layout shifts */
}
.user-message-box p {
  margin: 0;
}
.user-message-box strong {
  color: #555;
}
@media screen and (max-width: 1024px) {
  .score-board-module {
    min-width: 0px;
  }
}
</style>
