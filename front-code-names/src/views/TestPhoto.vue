<template>
  <div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

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

onBeforeUnmount(() => {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
});
</script>

<style scoped>
video {
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
}
img {
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  margin-top: 10px;
}
</style>
