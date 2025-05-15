// .eslintrc.js
module.exports = {
  // ...
  extends: [
    "plugin:vue/vue3-recommended",
    // autres extends selon ton stack
  ],
  globals: {
    defineProps: "readonly",
    defineEmits: "readonly",
    defineExpose: "readonly",
    withDefaults: "readonly",
  },
};
