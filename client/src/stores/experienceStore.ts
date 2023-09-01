import {defineStore} from "pinia";
import {useUserStore} from "@/stores/userStore";
import axios from "axios";
import {config} from "@/config";
import {ResponseBase} from "@/stores/common";


const apiUrl = config.apiUrl;

export class UploadResponse extends ResponseBase {
}

type UploadCallback = (response: UploadResponse) => void;

export const useExperienceStore = defineStore('experience', () => {
    const userStore = useUserStore();

    function uploadExperience(audioBlob, success: UploadCallback, failed: UploadCallback): void {
        const formData = new FormData();
        formData['file'] = audioBlob;
        const headers = {'Content-Type': 'multipart/form-data'}
        if (!userStore.addAuthenticationHeader(headers)) {
            failed({
                errors: [],
                isError: true,
                message: 'User is not authenticated'
            });
        }
        const postUrl = `${apiUrl}/experiences/audiorecord`;
        console.log(postUrl);
        axios.post(postUrl, formData, {headers})
            .then((res) => {
                console.log(res);
                success({
                    isError: false,
                    errors: [],
                    message: 'Upload OK'
                });
            }).catch((err) => {
            console.error(err);
            failed({
                isError: true,
                message: 'check the logs',
                errors: []
            });
        });
    }

    return {uploadExperience};
});