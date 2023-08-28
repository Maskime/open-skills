<script setup lang="ts">
import "bootstrap/dist/js/bootstrap.bundle.min.js"

import {Ref, ref} from "vue";
import Alert from "@/components/Alert.vue";
import {UserResponse, useUserStore} from "@/stores/userStore";


const userStore = useUserStore();

interface LoginForm {
  email: string;
  password: string;
  rememberMe: string[];
}

interface UserRegisterForm {
  name: string;
  firstName: string;
  email: string;
  password: string;
}

const loginForm: Ref<LoginForm> = ref({
  email: '',
  password: '',
  rememberMe: []
});

const registerForm: Ref<UserRegisterForm> = ref({
  name: '',
  firstName: '',
  email: '',
  password: ''
});

const registerClose = ref(null);

const showAlert = ref(false);
const alertMessage = ref<Alert>({
  level: 'info',
  msg: '',
  errors: []
});

function handleLogin() {
  //userStore.login(loginForm.value)
  console.log(loginForm)
}

function initRegisterForm() {
  registerForm.value.name = '';
  registerForm.value.firstName = '';
  registerForm.value.email = '';
  registerForm.value.password = '';
}

function handleRegister() {
  let registerPayload: UserRegisterForm = {
    name: registerForm.value.name,
    firstName: registerForm.value.firstName,
    email: registerForm.value.email,
    password: registerForm.value.password
  };
  userStore.createUser(registerPayload, handleUserCreateSuccess, handleUserCreateFailed);

}

function handleUserCreateFailed(response: UserResponse) {
  showAlert.value = true;
  alertMessage.value.msg = response.message;
  alertMessage.value.level = 'danger';
  alertMessage.value.errors = response.errors;
}

function handleUserCreateSuccess(response: UserResponse) {
  initRegisterForm();
  showAlert.value = true;
  alertMessage.value.msg = response.message;
  alertMessage.value.level = 'success';
  setTimeout(() => {
    handleClose();
    if (registerClose.value != null) {
      registerClose.value.click();
    }
  }, 1500)
}

function handleClose() {
  showAlert.value = false;
  alertMessage.value.msg = '';
  alertMessage.value.level = 'info';
}
</script>

<template>

  <div class="d-flex align-items-center py-4 bg-body-tertiary">
    <main class="form-signin w-100 m-auto">
      <form>
        <img class="mb-4" src="../assets/ptc.svg" alt="" height="57">
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

        <div class="form-floating">
          <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
          <label for="floatingInput">Email address</label>
        </div>
        <div class="form-floating">
          <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
          <label for="floatingPassword">Password</label>
        </div>

        <div class="form-check text-start my-3">
          <input class="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault">
          <label class="form-check-label" for="flexCheckDefault">
            Remember me
          </label>
        </div>
        <button class="btn btn-primary w-100 py-2" type="submit">Sign in</button>
        <p class="mt-5 mb-3 text-body-secondary">
          <a href="#" data-bs-toggle="modal" data-bs-target="#modalSignin">Register</a>
        </p>
      </form>
    </main>
  </div>

  <div class="modal fade" tabindex="-1" role="dialog"
       id="modalSignin">
    <div class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-header p-5 pb-4 border-bottom-0">
          <h1 class="fw-bold mb-0 fs-2">Sign up for free</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                  ref="registerClose" @click="handleClose"></button>
        </div>
        <div class="modal-body p-5 pt-0">
          <form class="">
            <div v-if="showAlert" class="form-floating mb-3">
              <alert v-bind="alertMessage"></alert>
            </div>
            <div class="form-floating mb-3">
              <input v-model="registerForm.email" type="email" class="form-control rounded-3" id="floatingInput"
                     placeholder="name@example.com">
              <label for="floatingInput">Email address</label>
            </div>
            <div class="form-floating mb-3">
              <input v-model="registerForm.firstName" type="text" class="form-control rounded-3" id="floatingInput"
                     placeholder="Your first name">
              <label for="floatingInput">First name</label>
            </div>
            <div class="form-floating mb-3">
              <input v-model="registerForm.name" type="text" class="form-control rounded-3" id="floatingInput"
                     placeholder="Your name">
              <label for="floatingInput">Name</label>
            </div>
            <div class="form-floating mb-3">
              <input v-model="registerForm.password" type="password" class="form-control rounded-3"
                     id="floatingPassword" placeholder="Password">
              <label for="floatingPassword">Password</label>
            </div>
            <button class="w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="button" @click="handleRegister">Sign up
            </button>
            <small class="text-body-secondary">By clicking Sign up, you agree to the terms of use.</small>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

.b-example-divider {
  width: 100%;
  height: 3rem;
  background-color: rgba(0, 0, 0, .1);
  border: solid rgba(0, 0, 0, .15);
  border-width: 1px 0;
  box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
}

.b-example-vr {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
}

.bi {
  vertical-align: -.125em;
  fill: currentColor;
}

.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
}

.nav-scroller .nav {
  display: flex;
  flex-wrap: nowrap;
  padding-bottom: 1rem;
  margin-top: -1px;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}

.btn-bd-primary {
  --bd-violet-bg: #712cf9;
  --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

  --bs-btn-font-weight: 600;
  --bs-btn-color: var(--bs-white);
  --bs-btn-bg: var(--bd-violet-bg);
  --bs-btn-border-color: var(--bd-violet-bg);
  --bs-btn-hover-color: var(--bs-white);
  --bs-btn-hover-bg: #6528e0;
  --bs-btn-hover-border-color: #6528e0;
  --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
  --bs-btn-active-color: var(--bs-btn-hover-color);
  --bs-btn-active-bg: #5a23c8;
  --bs-btn-active-border-color: #5a23c8;
}

.bd-mode-toggle {
  z-index: 1500;
}

html,
body {
  height: 100%;
}

.form-signin {
  max-width: 330px;
  padding: 1rem;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>