<script setup lang="ts">
import {ref} from "vue";
import axios from "axios";

const message = ref('Hello')

const path = 'http://localhost:5000/ping'
axios.get(path).then((res) => message.value = res.data).catch((err) => console.error(err));
</script>

<template>
  <div class="container">
    <button class="btn btn-primary">{{message}}</button>
  </div>
</template>

<style scoped>

</style>