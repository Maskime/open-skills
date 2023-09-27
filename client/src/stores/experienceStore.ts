import {defineStore} from "pinia";
import {useUserStore} from "@/stores/userStore";
import axios from "axios";
import {config} from "@/config";
import {ResponseBase} from "@/stores/common";
import {type Ref, ref} from "vue";


const apiUrl = config.apiUrl;

export class UploadResponse extends ResponseBase {
    taskId: number = 0;
}

export interface ExpRecord{
    date: string;
    url: string;
    task_id:number;
}

export class ExpRecordsResponse extends ResponseBase{
    records:ExpRecord[] = [];
}

type UploadCallback = (response: UploadResponse) => void;
type RecordingsCallback = (response: ExpRecordsResponse) => void;

export const useExperienceStore = defineStore('experience', () => {
    const userStore = useUserStore();
    const toResume: Ref<number> = ref(0)

    function uploadExperience(audioBlob: any, success: UploadCallback, failed: UploadCallback): void {
        const formData = new FormData();
        formData.append('file', audioBlob);
        const headers = {'Content-Type': 'multipart/form-data'}
        if (!userStore.addAuthenticationHeader(headers)) {
            failed({
                errors: [],
                isError: true,
                message: 'User is not authenticated',
                taskId: 0
            });
        }
        const postUrl = `${apiUrl}/experiences/audiorecord`;
        axios.post(postUrl, formData, {headers})
            .then((res) => {
                console.log(res);
                success({
                    isError: false,
                    errors: [],
                    message: 'Upload OK',
                    taskId: res.data.task_id
                });
            }).catch((err) => {
            console.error(err);
            failed({
                isError: true,
                message: 'check the logs',
                errors: [],
                taskId: 0
            });
        });
    }

    function getRecordings(success: RecordingsCallback, failed:RecordingsCallback) {
        const headers = {}
        if (!userStore.addAuthenticationHeader(headers)) {
            failed({
                errors: [],
                isError: true,
                message: 'User is not authenticated',
                records: []
            });
        }
        const audioUrl = `${apiUrl}/experiences/audiorecord`;
        axios.get(audioUrl, {headers})
            .then((res) => {
                let response = new ExpRecordsResponse();
                response.records = res.data.records
                success(response);
            })
            .catch((err) => {
                let response = new ExpRecordsResponse();
                response.isError = true;
                response.message = err.message;
                failed(response);
            });
    }

    return {uploadExperience, getRecordings, toResume};
});