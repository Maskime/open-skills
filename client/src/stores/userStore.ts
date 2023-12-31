import {defineStore} from "pinia";
import axios from "axios";
import {type Ref, ref} from "vue";
import {config} from "@/config";
import {ResponseBase} from "@/stores/common";

interface User {
    name: string;
    firstName: string;
    email: string;
    password: string;
}

export interface Login {
    email: string;
    password: string;
}


export class RegisterResponse extends ResponseBase {
}

export class LoginResponse extends ResponseBase {
    isAuthenticated: boolean = false;
    token: string = '';
    userEmail: string = '';
}

type RegisterCallback = (response: RegisterResponse) => void;
type LoginCallback = (response: LoginResponse) => void;

const path = config.apiUrl;

export const useUserStore = defineStore('user', () => {

    const authentToken: Ref<string> = ref('');
    const authentEmail: Ref<string> = ref('');

    function createResponseBaseError<T extends ResponseBase>(err: any, resp: T): T {
        console.error(err);
        if("response" in err) {
            let errors: string[];
            if (err.response.data.errors) {
                errors = err.response.data.errors;
            } else {
                errors = [];
            }
            if (err.response.data.exception) {
                errors.push(err.response.data.exception);
            }
            let message: string = err.response.data.message;
            resp.isError = true;
            resp.message = message;
            resp.errors = errors;
            return resp;
        }
        resp.isError = true;
        resp.message = `Une erreur technique est survenue : ${err.message}`;
        resp.errors = [];
        return resp;
    }

    function createUser(user: User, success: RegisterCallback, failed: RegisterCallback) {
        axios.post(path + '/users/register', user)
            .then((res) => {
                console.log(res.data);
                let response: RegisterResponse = {isError: false, message: res.data.message, errors: []}
                success(response);
            })
            .catch((err) => {
                const resp: RegisterResponse = new RegisterResponse();
                failed(createResponseBaseError(err, resp));
            });
    }

    function login(login: Login, success: LoginCallback, failed: LoginCallback) {
        axios.post(path + '/users/authenticate', login)
            .then((res) => {
                console.log(res.data);
                let response: LoginResponse = {
                    isAuthenticated: res.data.is_authenticated,
                    token: res.data.token,
                    userEmail: res.data.user_email,
                    errors: [],
                    isError: false,
                    message: res.data.message
                };
                authentEmail.value = response.userEmail;
                authentToken.value = response.token;
                success(response);
            })
            .catch((err) => {
                const resp: LoginResponse = new LoginResponse();
                let response = createResponseBaseError(err, resp);
                failed(response);
            });
    }

    function isAuthenticated(): boolean {
        return authentToken.value !== '';
    }

    function logout(): void {
        authentEmail.value = '';
        authentToken.value = '';
    }

    function addAuthenticationHeader(header: { [name: string]: string }): boolean {
        if (!isAuthenticated()) {
            return false;
        }
        header['Authorization'] = `Bearer ${authentToken.value}`;
        return true;
    }

return {createUser, login, authentEmail, authentToken, isAuthenticated, logout, addAuthenticationHeader};
});