import { createRouter, createWebHistory } from 'vue-router'


import Login from "@/views/Login.vue";
import Home from "@/views/Home.vue";
import {useUserStore} from "@/stores/userStore";
import LandingView from "@/views/LandingView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component:LandingView
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      beforeEnter(to, from, next){
        const userStore = useUserStore();
        if(!userStore.isAuthenticated()){
          next('/login');
        } else {
          next();
        }
      }
    }
  ]
})

export default router
