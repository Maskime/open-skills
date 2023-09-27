<script setup lang="ts">

import {toast} from "vue3-toastify";

interface ExtractionHeader {
  company_name: string;
  start_date: string;
  end_date: string;
  is_current_position: boolean;
  position_name: string;
}

interface ExtractionCompDetails {
  name: string;
  activities: string;
}

interface ExtractionProjectDetails {
  name: string;
  description: string;
  task_list: string[];
}

interface ExtractionTeamDetails {
  size: string;
  composition: string[];
}

interface ExtractionResult {
  header: ExtractionHeader;
  comp_details: ExtractionCompDetails;
  project_details: ExtractionProjectDetails;
  team_details: ExtractionTeamDetails;
  tech_list: string[]
}

import ComponentHeader from "@/components/ComponentHeader.vue";
import AudioRecorder from "@/components/AudioRecorder.vue";
import Alert from "@/components/Alert.vue";
import {onMounted, type Ref, ref} from "vue";
import {useAlertStore} from "@/stores/alertStore";
import {io, Socket} from "socket.io-client";
import {config} from "@/config"
import {useUserStore} from "@/stores/userStore";
import {useExperienceStore} from "@/stores/experienceStore";

const alertSore = useAlertStore();
const userStore = useUserStore();
const experienceStore = useExperienceStore();

const showRecorder: Ref<boolean> = ref(true);
const currentPhase: Ref<number> = ref(1);
const currentTaskId: Ref<number> = ref(-1);
const taskStatus: Ref<string> = ref('');
const taskDescription: Ref<string> = ref('Votre fichier audio nous a bien ete transmis.\nMerci de patienter pendant que nous le transcrivons.\n');
let socket: Socket | undefined;
const experienceTranscription: Ref<string> = ref('');
const extractionResult: Ref<ExtractionResult | null> = ref(null);


onMounted(() => {
  socket = io(config.apiUrl);
  socket.on('connect', () => {
    taskStatus.value = 'Client connecté au serveur websocket';
  });
  socket.on('invalid_taskid', () => {
    taskStatus.value = 'Le task id reçu par le serveur est erroné.';
    socket.disconnect();
  });
  socket.on('invalid_task_status', (data) => {
    console.log(data);
    taskStatus.value = 'Le status de la task est incorrecte';
    socket.disconnect();
  });
  socket.on('task_status', (data) => {
    console.log('task_status', data)
    taskStatus.value = data.status;
  });
  socket.on('transcription_received', (data) => {
    taskStatus.value = 'Transcription reçue.';
    experienceTranscription.value = data.text;
    currentPhase.value = 3;
  });
  socket.on('extraction_result', (data) => {
    currentPhase.value = 4;
    console.log(data);
    extractionResult.value = {
      header: data.header,
      comp_details: data.comp_details,
      project_details: data.project_details,
      team_details: data.team_details,
      tech_list: data.tech_details
    };
  });
  if (experienceStore.toResume != 0) {
    toast("Reprise à partir d'un enregistrement précédent.", {
      onClose: () => {
        const taskId: number = experienceStore.toResume;
        experienceStore.toResume = 0;
        audioRecordUploadSuccess(taskId);
      }
    });
  }
});

function audioRecordUploadFailed(errMessage: string) {
  showRecorder.value = false;
  alertSore.showError(`Une erreur a eu lieu pendant l'envoi de votre fichier audio au server: ${errMessage}`);
  setTimeout(() => {
    alertSore.clearAll();
    showRecorder.value = true;
  }, 2000);
}

function audioRecordUploadSuccess(taskId: number) {
  currentPhase.value = 2;
  currentTaskId.value = taskId;
  taskStatus.value = 'Fichier recu sur notre serveur';
  console.log('received task id', taskId);
  if (socket == undefined) {
    console.error("Could not initialize socket connection");
    return;
  }
  socket.emit('audio_transcription', {task_id: taskId, token: userStore.authentToken});

}

function startExtraction() {
  currentPhase.value = 2;
  taskDescription.value = "Nous commencons maintenant l'extraction des informations que vous nous avez fournies\n";
  taskStatus.value = "Transmission a notre serveur";
  socket.emit('start_extraction',
      {
        task_id: currentTaskId.value,
        token: userStore.authentToken,
        transcription: experienceTranscription.value
      });
}

</script>

<template>
  <ComponentHeader>Nouvelle expérience</ComponentHeader>
  <div v-if="currentPhase == 1" class="container">
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
        <AudioRecorder
            v-if="showRecorder"
            @upload-failed="audioRecordUploadFailed"
            @upload-success="audioRecordUploadSuccess"></AudioRecorder>
        <alert></alert>
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
  <div v-if="currentPhase == 2" class="container">
    <div class="alert alert-success" role="alert">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      {{ taskDescription }}<br>
      <i>{{ taskStatus }}</i>
    </div>
  </div>
  <div v-if="currentPhase == 3" class="container">
    <form>
      <div class="mb-lg-3">
        <textarea class="form-control" rows="5" v-model="experienceTranscription"></textarea>
      </div>
      <button type="button" class="btn btn-primary" @click="startExtraction">Demarrer l'extraction de donnees.
      </button>
    </form>
  </div>
  <div v-if="currentPhase == 4" class="container">
    <div class="row">
      <div class="col-8">{{ extractionResult.header.company_name }}</div>
      <div class="col-2">{{ extractionResult.header.start_date }}</div>
      <div class="col-2">{{ extractionResult.header.end_date }}</div>
    </div>
    <div class="row">
      <div class="col">{{ extractionResult.header.position_name }}</div>
    </div>
    <div class="row">
      <div class="col">
        <p>{{ extractionResult.project_details.name }}</p>
        <p>{{ extractionResult.project_details.description }}</p>
        <p>Tâches effectuées:</p>
        <ul>
          <li v-for="task in extractionResult.project_details.task_list">{{ task }}</li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>Composition de l'équipe:</p>
        <ul>
          <li v-for="team in extractionResult.team_details.composition">{{ team }}</li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>Environnement technique:</p>
        <ul>
          <li v-for="tech in extractionResult.tech_list">{{ tech }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>