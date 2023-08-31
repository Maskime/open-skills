<script setup lang="ts">

import {computed, ref} from "vue";
import {useAlertStore} from "@/stores/alertStore";


const show = ref(false);
const msg = ref('');
const level = ref('');
const errors = ref([])

const alertClass = computed(() => {
  if (level.value) {
    return 'alert-' + level.value;
  }
  return 'alert-info';
});

const alertStore = useAlertStore();
alertStore.$subscribe((mutation, state) => {
  show.value = state.show;
  console.log(state);
  if (show.value) {
    msg.value = state.message;
    level.value = state.level;
    errors.value = state.errors
  } else {
    msg.value = '';
    level.value = '';
    errors.value = [];
  }
});

function clearMessage(){
  alertStore.clearAll();
}
</script>

<template>
  <div v-if="show" class="alert alert-dismissible fade show" :class="alertClass" role="alert">{{ msg || 'it works !' }}
    <ul>
      <li v-for="error in errors">{{ error }}</li>
    </ul>
    <button @click="clearMessage" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>
</template>

<style scoped>

</style>