export function noError() {
    const error = document.getElementsByClassName("error-message");
    if (error.length == 1) {
        error[0].parentNode.removeChild(error[0]);
    }
}