import {defineStore} from "pinia";
import axios from "axios";

interface User {
    name: string;
    firstName: string;
    email: string;
    password: string;
}

interface Login {
    email: string;
    password: string;
}

export interface UserResponse {
    isError: boolean;
    message: string;
    errors: string[];
}

type CallbackFunction = (response: UserResponse) => void;

const path = 'http://localhost:5000/';

export const useUserStore = defineStore('user', () => {
    function createUser(user: User, success: CallbackFunction, failed: CallbackFunction) {
        axios.post(path + '/users/register', user)
            .then((res) => {
                console.log(res.data);
                let response: UserResponse = {isError: false, message: res.data.message, errors: []}
                success(response);
            })
            .catch((err) => {
                let response: UserResponse = {isError: true, message: err.data.response.data.message, errors: err.data.response.data.errors};
                failed(response);
            });
    }

    function login(login: Login, success: CallbackFunction, failed: CallbackFunction) {
        axios.post(path + '/users/login', login)
            .then((res) => {

            })
            .catch((err) => {})
    }

    return {createUser, login};
});