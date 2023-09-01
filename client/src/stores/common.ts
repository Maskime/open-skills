export class ResponseBase {
    isError: boolean = false;
    message: string = '';
    errors: string[] = [];
}