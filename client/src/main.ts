import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "bootstrap-icons/font/bootstrap-icons.css"
import 'vue3-toastify/dist/index.css';

import { createApp } from 'vue'
import {createPinia} from "pinia";
import App from './App.vue'
import router from './router'
import VueCookies from "vue-cookies";

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueCookies)
app.mount('#app')
