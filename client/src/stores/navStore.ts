import {defineStore} from "pinia";
import type {Ref} from "vue";
import {ref} from "vue";

export const useNavStore = defineStore('nav', () => {
    const currentComponent: Ref<string> = ref('');

    return {currentComponent};
});