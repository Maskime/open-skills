import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "bootstrap-icons/font/bootstrap-icons.css"

import { createApp } from 'vue'
import {createPinia} from "pinia";
import App from './App.vue'
import router from './router'

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.mount('#app')
