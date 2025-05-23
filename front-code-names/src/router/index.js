import { createRouter, createWebHistory } from "vue-router";
import CreateGame from "../views/CreateGame.vue";
import GameView from "../views/GameView.vue";
import TestPhoto from "../views/TestPhoto.vue";

const routes = [
  {
    path: "/",
    name: "CreateGame",
    component: CreateGame,
  },
  {
    path: "/game/:gameId",
    name: "GameView",
    component: GameView,
    props: true, // Pass route params as props to the component
  },
  {
    path: "/test",
    name: "TestPhoto",
    component: TestPhoto,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
