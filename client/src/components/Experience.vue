<script setup lang="ts">

import ComponentHeader from "@/components/ComponentHeader.vue";
import AudioRecorder from "@/components/AudioRecorder.vue";


</script>

<template>
  <ComponentHeader>Nouvelle expérience</ComponentHeader>
  <div class="container">
    <div class="row">
      <div class="alert alert-primary" role="alert">
        Enregistrez votre expérience. Vérifier que vous parlez de l'ensemble des points contenu dans la partie "Script"
        de cette page.
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="border-bottom">
          <h2>Enregistreur</h2>
        </div>
        <AudioRecorder></AudioRecorder>
      </div>
      <div class="col">
        <div class="border-bottom">
          <h2>Script</h2>
        </div>
        Voici la liste des choses que vous devez énoncer pendant votre enregistrement. <br>
        Essayez de rester cohérent pendant votre enregistrement.
        <ul>
          <li>Nom de l'entrepise</li>
          <li>Descriptif rapide de l'activité de l'entreprise</li>
          <li>Nom du poste que vous avez occupé pendant la mission</li>
          <li>Date de début et fin de la mission (le mois et l'année sont suffisant, pas la peine de retrouver le
            jour.)
          </li>
          <li>Nom du projet sur lequel vous avez travaillé</li>
          <li>Les tâches que vous avez effectuées pendant la mission</li>
          <li>La composition de l'équipe au sein de laquelle vous avez travaillé</li>
          <li>Description de l'environnement technique durant la mission</li>
        </ul>
        Pas besoin de formalisme particulier, parlez librement, comme si vous parliez à un humain.
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>