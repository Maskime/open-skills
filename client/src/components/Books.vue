<script setup lang="ts">

import {ref} from "vue";
import axios from "axios";

interface Book {
  title: string;
  author: string;
  read: boolean;
}

const path = 'http://localhost:5000/books'
const books = ref([])

const activeAddBookModal = ref(false)

const addBookForm = ref({
  title: '',
  author: '',
  read: []
})

function getBooks() {
  axios.get(path).then((res) => {
    books.value = res.data.books
  }).catch((err) => console.error(err));
}


function toggleAddBookModal() {
  const body = document.querySelector('body');
  if (body == null) {
    console.error('could not find the modal body')
    return;
  }
  activeAddBookModal.value = !activeAddBookModal.value;
  if (activeAddBookModal.value) {
    body.classList.add('modal-open');
  } else {
    body.classList.remove('modal-open');
  }
}

function addBook(payload: Book) {
  axios.post(path, payload).then(() => {
    getBooks()
  }).catch((err) => {
    console.error(err);
    getBooks()
  })
}

function initForm() {
  addBookForm.value.title = '';
  addBookForm.value.author = '';
  addBookForm.value.read = [];
}

function handleAddSubmit() {
  toggleAddBookModal();
  let read = false;
  if (addBookForm.value.read[0]) {
    read = true;
  }
  const payload = {
    title: addBookForm.value.title,
    author: addBookForm.value.author,
    read: read
  }
  addBook(payload);
  initForm();
}

function handleAddReset() {
  initForm();
}

getBooks();
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr>
        <br> <br>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddBookModal">Add Book</button>
        <br> <br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th class="col">Title</th>
            <th class="col">Author</th>
            <th class="col">Read?</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(book, index) in books" :key="index">
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>
              <span v-if="book.read">Yes</span>
              <span v-else>No</span>
            </td>
            <td>
              <div class="btn btn-group" role="group">
                <button class="btn btn-sm btn-warning">Update</button>
                <button class="btn btn-sm btn-danger">Danger</button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div
      ref="addBookModal"
      class="modal fade"
      :class="{show: activeAddBookModal, 'd-block': activeAddBookModal}"
      tabindex="-1"
      role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add a new book</h5>
          <button
              type="button"
              class="btn-close"
              data-miss="modal"
              aria-label="Close"
              @click="toggleAddBookModal">
            <span></span>
          </button>
        </div>
        <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="addBookTitle" class="form-label">Title:</label>
            <input
                type="text"
                class="form-control"
                id="addBookTitle"
                v-model="addBookForm.title"
                placeholder="Enter title">
          </div>
          <div class="mb-3">
            <label for="addBookAuthor" class="form-label">Author:</label>
            <input
                type="text"
                class="form-control"
                id="addBookAuthor"
                v-model="addBookForm.author"
                placeholder="Enter author">
          </div>
          <div class="mb-3 form-check">
            <input type="checkbox"
                   id="addBookRead"
                   v-model="addBookForm.read" class="form-check-input">
            <label for="addBookRead" class="form-check-label">Read?</label>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-sm btn-primary" @click="handleAddSubmit">Submit</button>
        <button type="button" class="btn btn-sm btn-danger" @click="handleAddReset">Reset</button>
      </div>
      </div>

    </div>
  </div>
  <div v-if="activeAddBookModal" class="modal-backdrop fade show"/>
</template>

<style scoped>

</style>