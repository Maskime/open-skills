<script setup lang="ts">

import ComponentHeader from "@/components/ComponentHeader.vue";
import {useNavStore} from "@/stores/navStore";
import {ExpRecord, ExpRecordsResponse, useExperienceStore} from "@/stores/experienceStore";
import {onMounted, ref, type Ref} from "vue";
import {useUserStore} from "@/stores/userStore";
const navStore = useNavStore();
const experienceStore = useExperienceStore();
const userStore = useUserStore();

const records:Ref<ExpRecord[]> = ref([]);
function recordsAcquired(resp: ExpRecordsResponse){
  records.value = resp.records;
}
onMounted(() => {
  experienceStore.getRecordings(recordsAcquired, (resp: ExpRecordsResponse) => {
    console.error(resp.message);
  });
});
function newExperience(){
  navStore.currentComponent = 'Experience';
}

function audioUrl(url:string){
  const audio = `http://localhost:5000${url}?token=${userStore.authentToken}`;
  console.log(audio);
  return audio;
}

function resume(task_id:number){
  experienceStore.toResume = task_id;
  navStore.currentComponent = 'Experience';
}

</script>

<template>
  <ComponentHeader>Expériences</ComponentHeader>
  <h2>Liste des Expériences enregistrées</h2>
  <button type="button" class="btn btn-primary" @click="newExperience">Ajouter une expérience</button>
  <h3>Enregistrements non complétés</h3>
  <div class="table-responsive small">
    <table class="table table-striped table-sm">
      <thead>
    <tr>
      <th scope="col">Date enregistrement</th>
      <th scope="col">Enregistrement</th>
      <th>&nbsp;</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="record in records">
      <td>{{record.date}}</td>
      <td>
        <audio controls>
          <source :src="audioUrl(record.url)" type="audio/x-wav">
        </audio>
        </td>
      <td>
        <button class="btn bi-send btn-outline-primary" @click="resume(record.task_id)"></button>
      </td>
    </tr>
    </tbody>
    </table>

  </div>
<!--  <div class="table-responsive small">-->
<!--    <table class="table table-striped table-sm">-->
<!--      <thead>-->
<!--      <tr>-->
<!--        <th scope="col">#</th>-->
<!--        <th scope="col">Entreprise</th>-->
<!--        <th scope="col">Projet</th>-->
<!--        <th scope="col">Début</th>-->
<!--        <th scope="col">Fin</th>-->
<!--      </tr>-->
<!--      </thead>-->
<!--      <tbody>-->
<!--      <tr>-->
<!--        <td>1,001</td>-->
<!--        <td>random</td>-->
<!--        <td>data</td>-->
<!--        <td>placeholder</td>-->
<!--        <td>text</td>-->
<!--      </tr>-->
<!--      </tbody>-->
<!--    </table>-->
<!--  </div>-->
</template>

<style scoped>

</style>