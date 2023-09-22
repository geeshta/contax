<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);
const increment = () => {
  count.value = count.value + 1;
};
</script>

<template>
  <div class="card">
    <button @click="increment" id="counter" type="button">count is {{ count }}</button>
  </div>
</template>

<style scoped>
.card {
  padding: 2em;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #1a1a1a;
  cursor: pointer;
  transition: border-color 0.25s;
}
button:hover {
  border-color: #646cff;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

@media (prefers-color-scheme: light) {
  button {
    background-color: #f9f9f9;
  }
}
</style>
