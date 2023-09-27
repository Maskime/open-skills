<script setup lang="ts">
import Header from "@/components/Header.vue";
import SideMenu from "@/components/SideMenu.vue";
import {ref, shallowRef} from "vue";
import {useNavStore} from "@/stores/navStore";
import Experiences from "@/components/Experiences.vue";
import Experience from "@/components/Experience.vue";

const navStore = useNavStore();

const components = {
  'Experiences': Experiences,
  'Experience': Experience
}

const currentComponent = shallowRef(Experiences);
navStore.$subscribe((mutation, state) => {
    currentComponent.value = components[state.currentComponent];
    console.log(`Switching to ${currentComponent.value}`);
});
</script>

<template>
  <Header></Header>

  <div class="container-fluid">
    <div class="row">
      <SideMenu></SideMenu>
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <component :is="currentComponent"></component>
      </main>
    </div>
  </div>
</template>

<style scoped>

@media (min-width: 768px) {
  .sidebar .offcanvas-lg {
    position: -webkit-sticky;
    position: sticky;
    top: 48px;
  }
  .navbar-search {
    display: block;
  }
}





</style>