<template>
  <div id="nav"></div>
  <router-view />
</template>

<style>
body {
  font-family: sans-serif;
  margin: 0;
  background-color: #f4f4f4;
  color: #333;
}

#app {
  padding: 20px;
}

/* Basic button styling */
button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
}

.loading {
  font-style: italic;
}
</style>
