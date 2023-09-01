<script setup lang="ts">
import {useUserStore} from "@/stores/userStore";
import {useRouter} from "vue-router";
import {toast} from "vue3-toastify";
import type {Ref} from "vue";
import {ref} from "vue";
import {useNavStore} from "@/stores/navStore";
import Profile from "@/components/Profile.vue";

interface NavLink {
  label: string;
  isActive: boolean;
  iconClass: string;
  destComponent: string;
}

const userStore = useUserStore();
const router = useRouter();
const navStore = useNavStore();

const menuItems: Ref<NavLink[]> = ref<NavLink[]>([]);

menuItems.value.push({
      label: 'Profile',
      iconClass: 'bi-house',
      isActive: false,
      destComponent: 'Profile'
    },
    {
      label: 'Expériences',
      iconClass: 'bi-emoji-laughing',
      isActive: false,
      destComponent: 'Experiences'
    },
    {
      label: 'Technologies',
      iconClass: 'bi-cpu',
      isActive: false,
      destComponent: 'Technologies'
    }
);

function logout() {
  userStore.logout();
  toast('Login out !', {
    onClose: () => {
      router.push({name: 'login'});
    }
  });
}

function changeComponent(destComponent:any){
  console.log(destComponent);
  navStore.currentComponent = destComponent;
}
</script>

<template>
  <div class="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary">
    <div class="offcanvas-md offcanvas-end bg-body-tertiary" tabindex="-1" id="sidebarMenu"
         aria-labelledby="sidebarMenuLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="sidebarMenuLabel">Open Skills</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" data-bs-target="#sidebarMenu"
                aria-label="Close"></button>
      </div>
      <div class="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto">
        <ul class="nav flex-column">
          <li v-for="navItem in menuItems" class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2" :class="navItem.iconClass" aria-current="page" @click="changeComponent(navItem.destComponent)" href="#">
              {{ navItem.label }}
            </a>
          </li>
        </ul>

        <hr class="my-3">

        <ul class="nav flex-column mb-auto">
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2 bi-gear-wide-connected" href="#">
              Settings
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2 bi-door-closed" href="#" @click="logout">
              Sign out
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar .nav-link {
  font-size: .875rem;
  font-weight: 500;
}

.sidebar .nav-link.active {
  color: #2470dc;
}

.sidebar-heading {
  font-size: .75rem;
}

/*
 * Sidebar
 */

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