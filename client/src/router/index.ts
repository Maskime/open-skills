import { createRouter, createWebHistory } from 'vue-router'

import Ping from "@/components/Ping.vue";
import Books from '@/components/Books.vue';
import Login from "@/views/Login.vue";
import RegisterUser from "@/views/RegisterUser.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/books',
      name: 'books',
      component: Books
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/users/register',
      name: 'users_register',
      component: RegisterUser
    }
  ]
})

export default router
