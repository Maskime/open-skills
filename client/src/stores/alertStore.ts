import {defineStore} from "pinia";
import {ref} from "vue";

export const useAlertStore = defineStore('alert', () => {

    const message = ref('');
    const level = ref('');
    const errors = ref<string[]>([]);
    const show = ref(false);

    function showSuccess(msg: string){
        message.value = msg;
        level.value = 'success';
        show.value = true;
    }

    function showError(msg: string, errs?: string[]){
        message.value = msg;
        level.value = 'danger';
        if(errs){
            errs.forEach(value => errors.value.push(value));
        }
        show.value = true;
    }

    function clearAll(){
        message.value = '';
        level.value = '';
        errors.value = [];
        show.value = false;
    }
    return {showSuccess, showError, clearAll, message, level, errors, show};
});