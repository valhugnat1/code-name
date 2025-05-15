import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios"; // Import axios

const app = createApp(App);

// Configure a base URL for Axios (optional, but good practice)
axios.defaults.baseURL = "http://localhost:8000"; // Your backend URL

app.use(router);
app.mount("#app");
