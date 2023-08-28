<script setup lang="ts">

import {computed} from "vue";

const props = defineProps({
  msg: {
    type: String,
    required: true
  },
  level: {
    validator(value: string){
      if(value == null){
        return true;
      }
      return ['success', 'danger', 'warning', 'info'].includes(value);
    }
  },
  errors: {
    type: Array,
    required: false
  }
});

const alertClass = computed(() => {
  if (props.level){
    return 'alert-' + props.level;
  }
  return 'alert-info';
});

</script>

<template>
<div class="alert" :class="alertClass" role="alert">{{msg || 'it works !'}}
  <ul>
    <li v-for="error in errors">{{error}}</li>
  </ul>
</div>
</template>

<style scoped>

</style>