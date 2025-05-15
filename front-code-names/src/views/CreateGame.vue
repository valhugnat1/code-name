<template>
  <div class="create-game-container">
    <h1>Create Codenames Game</h1>

    <div class="input-options">
      <!-- Option Photo (existante) -->
      <div class="photo-module">
        <!-- <div>
          <video ref="video" autoplay playsinline></video>
          <canvas ref="canvas" style="display: none"></canvas>
          <div>
            <button @click="startCamera">Démarrer la caméra</button>
            <button @click="takePhoto">Prendre une photo</button>
          </div>
          <div v-if="photo">
            <h3>Photo capturée :</h3>
            <img :src="photo" alt="Captured photo" />
          </div>
        </div> -->
        <button @click="triggerFileInput" class="photo-button">
          <span class="icon">📷</span> Scan Words from the Photo
        </button>
        <input
          type="file"
          accept="image/*"
          capture="environment"
          ref="fileInput"
          @change="handleImageUpload"
          style="display: none"
        />
        <div v-if="imagePreviewUrl" class="image-preview-container">
          <p>Image Preview:</p>
          <img :src="imagePreviewUrl" alt="Preview" class="image-preview" />
        </div>
        <div v-if="isAnalysing" class="loading-analysis">
          <p>Analysing image, please wait...</p>
          <div class="spinner"></div>
        </div>
      </div>

      <!-- Nouvelle option File Upload -->
      <div class="file-module">
        <button @click="triggerTextFileInput" class="file-button">
          <span class="icon">📄</span> Upload Words from File
        </button>
        <input
          type="file"
          accept=".txt,.csv"
          ref="textFileInput"
          @change="handleFileUpload"
          style="display: none"
        />
        <div v-if="uploadedFileName" class="file-info">
          <p>File uploaded: {{ uploadedFileName }}</p>
        </div>
        <div v-if="isParsingFile" class="loading-analysis">
          <p>Parsing file, please wait...</p>
          <div class="spinner"></div>
        </div>
      </div>
    </div>

    <!-- Section des mots extraits (commune aux deux méthodes) -->
    <div v-if="extractedWords.length > 0" class="extracted-words-container">
      <h2>Extracted Words:</h2>
      <ul class="extracted-words-list">
        <li v-for="(word, index) in extractedWords" :key="index">
          {{ word }}
        </li>
      </ul>
      <p v-if="extractedWords.length !== 25" class="warning-text">
        Warning: {{ extractedWords.length }} words were extracted. The game
        requires 25 words. The game will be launched with these words, padded or
        truncated if necessary.
      </p>
    </div>

    <button
      @click="handleCreateGame"
      :disabled="isLoading || isAnalysing || isParsingFile"
      class="launch-button"
    >
      {{
        isLoading
          ? "Creating..."
          : extractedWords.length > 0
          ? "Launch Game with Extracted Words"
          : "Launch Game with Default Words"
      }}
    </button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios"; // Vous l'utiliserez pour l'appel à GPT-4o et pour la création du jeu

const video = ref(null);
const canvas = ref(null);
const photo = ref(null);
let stream = null;

const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.value.srcObject = stream;
  } catch (error) {
    console.error("Erreur accès caméra :", error);
  }
};

const takePhoto = () => {
  const width = video.value.videoWidth;
  const height = video.value.videoHeight;

  canvas.value.width = width;
  canvas.value.height = height;

  const context = canvas.value.getContext("2d");
  context.drawImage(video.value, 0, 0, width, height);

  photo.value = canvas.value.toDataURL("image/png");
};

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
const words = ref([...defaultWords]); // Sera mis à jour par les mots extraits
const isLoading = ref(false);
const errorMessage = ref("");

// Références pour le module photo
const fileInput = ref(null); // Référence à l'élément input file
const imagePreviewUrl = ref(""); // URL pour l'aperçu de l'image
const isAnalysing = ref(false); // État pendant l'analyse de l'image
const extractedWords = ref([]); // Mots extraits de l'image ou du fichier

// Nouvelles références pour le module fichier
const textFileInput = ref(null); // Référence à l'élément input file pour les fichiers texte
const uploadedFileName = ref(""); // Nom du fichier téléchargé
const isParsingFile = ref(false); // État pendant l'analyse du fichier

// Surveiller les changements dans extractedWords pour mettre à jour words
watch(extractedWords, (newWords) => {
  if (newWords && newWords.length > 0) {
    // S'assurer qu'il y a exactement 25 mots
    const adjustedWords = new Array(25).fill("EMPTY");
    for (let i = 0; i < 25; i++) {
      if (i < newWords.length) {
        adjustedWords[i] = newWords[i];
      }
    }
    words.value = adjustedWords;
  } else {
    words.value = [...defaultWords]; // Revenir aux mots par défaut si aucune extraction
  }
});

// Fonctions pour le module photo
function triggerFileInput() {
  extractedWords.value = []; // Réinitialiser les mots extraits précédents
  imagePreviewUrl.value = ""; // Réinitialiser l'aperçu
  uploadedFileName.value = ""; // Réinitialiser le nom du fichier téléchargé
  if (fileInput.value) {
    fileInput.value.click(); // Ouvre le sélecteur de fichier/caméra
  }
}

async function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) {
    return;
  }

  // Afficher un aperçu de l'image
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreviewUrl.value = e.target.result;
  };
  reader.readAsDataURL(file);

  isAnalysing.value = true;
  errorMessage.value = "";

  try {
    // Appel à la fonction extractTextFromImage avec le fichier sélectionné
    const words = await extractTextFromImage(file);

    console.log("GPT-4o analysis complete. Words:", words);
    extractedWords.value = words;
  } catch (error) {
    console.error("Error analysing image:", error);
    errorMessage.value = `Failed to analyse image: ${error.message}. Using default words.`;
    extractedWords.value = []; // Réinitialiser en cas d'erreur
    words.value = [...defaultWords]; // S'assurer que words a les valeurs par défaut
  } finally {
    isAnalysing.value = false;
    // Réinitialiser la valeur du champ de fichier pour permettre la re-sélection du même fichier
    if (fileInput.value) {
      fileInput.value.value = "";
    }
  }
}

// Nouvelles fonctions pour le module fichier
function triggerTextFileInput() {
  extractedWords.value = []; // Réinitialiser les mots extraits précédents
  imagePreviewUrl.value = ""; // Réinitialiser l'aperçu de l'image
  uploadedFileName.value = ""; // Réinitialiser le nom du fichier téléchargé
  if (textFileInput.value) {
    textFileInput.value.click(); // Ouvre le sélecteur de fichier texte
  }
}

async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) {
    return;
  }

  uploadedFileName.value = file.name;
  isParsingFile.value = true;
  errorMessage.value = "";

  try {
    // Lecture et traitement du fichier
    const words = await extractWordsFromFile(file);

    console.log("File analysis complete. Words:", words);
    extractedWords.value = words;
  } catch (error) {
    console.error("Error processing file:", error);
    errorMessage.value = `Failed to process file: ${error.message}. Using default words.`;
    extractedWords.value = []; // Réinitialiser en cas d'erreur
    words.value = [...defaultWords]; // S'assurer que words a les valeurs par défaut
  } finally {
    isParsingFile.value = false;
    // Réinitialiser la valeur du champ de fichier pour permettre la re-sélection du même fichier
    if (textFileInput.value) {
      textFileInput.value.value = "";
    }
  }
}

// Fonction pour extraire des mots à partir d'un fichier texte ou CSV
async function extractWordsFromFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const content = e.target.result;
        let words = [];

        // Vérification de l'extension du fichier
        if (file.name.toLowerCase().endsWith(".csv")) {
          // Traitement CSV simple (séparation par virgules)
          const lines = content.split(/\r?\n/);
          lines.forEach((line) => {
            if (line.trim()) {
              // Diviser par virgules et nettoyer les espaces
              const lineWords = line
                .split(",")
                .map((word) => word.trim())
                .filter((word) => word);
              words = words.concat(lineWords);
            }
          });
        } else {
          // Traitement fichier texte (un mot par ligne)
          const lines = content.split(/\r?\n/);
          words = lines.map((line) => line.trim()).filter((word) => word);
        }

        // Limite à 25 mots maximum
        resolve(words.slice(0, 25));
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => {
      reject(new Error("Error reading file"));
    };

    reader.readAsText(file);
  });
}

// Il est préférable de stocker la clé API dans une variable d'environnement
// Ne jamais exposer une clé API directement dans le code front-end
// Idéalement, cette requête devrait être effectuée depuis votre backend
const OPENAI_API_KEY = process.env.VUE_APP_OPENAI_API_KEY;

async function extractTextFromImage(imageFile) {
  try {
    // Convert the image to base64
    let base64Image = await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(",")[1];
        resolve(base64);
      };
      reader.readAsDataURL(imageFile);
    });

    // Prepare the request to OpenAI API
    const payload = {
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content:
            "You are an OCR tool. Extract all words from the image and return them as a JSON array. Don't include any explanations, just return a valid JSON array of strings.",
        },
        {
          role: "user",
          content: [
            {
              type: "text",
              text: 'Extract all words from this image and return them as a JSON array. Format: {"words": ["word1", "word2", "word3", ...]}',
            },
            {
              type: "image_url",
              image_url: {
                url: `data:image/${imageFile.type};base64,${base64Image}`,
              },
            },
          ],
        },
      ],
      response_format: { type: "json_object" },
    };

    console.log(OPENAI_API_KEY);

    // Make the API request
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(
        `API request failed with status ${
          response.status
        }: ${await response.text()}`
      );
    }

    const data = await response.json();

    // Parse the response to get the words array
    const content = data.choices[0].message.content;
    const wordsObject = JSON.parse(content);

    // Return the words array
    return wordsObject.words || [];
  } catch (error) {
    console.error("Error extracting text from image:", error);
    throw error;
  }
}

async function handleCreateGame() {
  isLoading.value = true;
  errorMessage.value = "";

  // Utiliser `words.value` qui est maintenant mis à jour par `extractedWords` ou les mots par défaut
  const gameWords = words.value.filter((word) => word && word.trim() !== "");

  if (gameWords.length !== 25) {
    errorMessage.value = `Please ensure 25 words are available. Currently ${gameWords.length}. Adjusting to 25.`;
    // Ajustement pour toujours avoir 25 mots, en remplissant avec "VIDE" ou en tronquant
    const finalWords = new Array(25).fill("VIDE");
    for (let i = 0; i < 25; i++) {
      if (i < gameWords.length) {
        finalWords[i] = gameWords[i];
      }
    }
    words.value = finalWords; // Mettre à jour la source principale des mots
    // Ne pas arrêter le processus, laisser le backend gérer/valider
  }

  try {
    // L'API backend attend un tableau de 25 chaînes de caractères pour 'cards'
    const response = await axios.post("/game", { cards: words.value });
    if (response.data && response.data.game_id) {
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
          .map((d) => `${d.loc ? d.loc.join("->") : "Error"}: ${d.msg}`)
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

/* Style pour les conteneurs d'options */
.input-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

/* Styles pour le module photo */
.photo-module,
.file-module {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.photo-button,
.file-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 15px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  justify-content: center;
}

/* Couleur différente pour le bouton de fichier */
.file-button {
  background-color: #6c757d;
}

.file-button:hover {
  background-color: #5a6268;
}

.photo-button .icon,
.file-button .icon {
  font-size: 1.2em;
}

.photo-button:hover {
  background-color: #0056b3;
}

.image-preview-container,
.file-info {
  margin-top: 15px;
  text-align: center;
}

.image-preview {
  max-width: 100%;
  max-height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
}

.loading-analysis {
  margin-top: 15px;
  color: #555;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #007bff;
  animation: spin 1s ease infinite;
  margin: 10px auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.extracted-words-container {
  margin-top: 20px;
  text-align: left;
  padding: 10px;
  background-color: #e9f5ff;
  border-radius: 4px;
}

.extracted-words-container h2 {
  font-size: 1.2em;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.extracted-words-list {
  list-style-type: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(100px, 1fr)
  ); /* Responsive grid */
  gap: 8px;
  font-size: 0.95em;
}

.extracted-words-list li {
  background-color: #fff;
  padding: 8px;
  border: 1px solid #cce7ff;
  border-radius: 3px;
  text-align: center;
}

.warning-text {
  color: #e67e22; /* Orange warning color */
  font-size: 0.9em;
  margin-top: 10px;
  text-align: center;
}

.launch-button {
  /* Styles pour le bouton principal */
  background-color: #5cb85c;
  color: white;
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.launch-button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.launch-button:hover:not(:disabled) {
  background-color: #4cae4c;
}

.error {
  color: #d9534f; /* Rouge pour les erreurs */
  margin-top: 15px;
  font-weight: bold;
}

/* Media queries pour la mise en page responsive */
@media (min-width: 768px) {
  .input-options {
    flex-direction: row;
  }

  .photo-module,
  .file-module {
    width: 50%;
  }
}
</style>
