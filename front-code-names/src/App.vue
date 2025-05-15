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

/* Smartphone landscape mode optimizations */
@media screen and (max-width: 1024px) {
  body {
    width: fit-content;
  }
}

/* Smartphone landscape mode optimizations */
@media screen and (orientation: landscape) and (max-width: 1024px) {
  #app {
    padding: 5px; /* Reduced padding from 20px to 5px */
  }

  button {
    padding: 5px 10px; /* Reduced button padding */
    font-size: 0.9em; /* Slightly smaller font for buttons */
  }

  .error {
    margin-top: 5px; /* Reduced error margin */
  }
}

/* Even more compact for very small screens */
@media screen and (orientation: landscape) and (max-height: 500px) {
  body {
    width: fit-content;
  }
  #app {
    padding: 3px; /* Minimal padding */
  }

  button {
    padding: 3px 8px; /* Minimal button padding */
    font-size: 0.85em;
  }
}
</style>
