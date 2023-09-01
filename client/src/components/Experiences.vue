<script setup lang="ts">

import ComponentHeader from "@/components/ComponentHeader.vue";
import {useNavStore} from "@/stores/navStore";
const navStore = useNavStore();
function newExperience(){
  navStore.currentComponent = 'Experience';
}
</script>

<template>
  <ComponentHeader>Expériences</ComponentHeader>
  <h2>Liste des Expériences enregistrées</h2>
  <button type="button" class="btn btn-primary" @click="newExperience">Ajouter une expérience</button>
  <div class="table-responsive small">
    <table class="table table-striped table-sm">
      <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Entreprise</th>
        <th scope="col">Projet</th>
        <th scope="col">Début</th>
        <th scope="col">Fin</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td>1,001</td>
        <td>random</td>
        <td>data</td>
        <td>placeholder</td>
        <td>text</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>

</style>