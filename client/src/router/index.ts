import { createRouter, createWebHistory } from 'vue-router'


import Login from "@/views/Login.vue";
import RegisterUser from "@/views/RegisterUser.vue";
import Home from "@/views/Home.vue";
import {useUserStore} from "@/stores/userStore";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/users/register',
      name: 'users_register',
      component: RegisterUser
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
