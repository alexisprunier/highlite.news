import { getApiURL } from "./env";


export async function getRequest(url, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url, {
        method: "GET",
        headers: new Headers({
            Accept: "application/json, text/html",
            credentials: "include",
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
        })
    }).then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status === 403) {
            window.location.replace("/?status=expiredSession");
        } else {
            if (catchBadResponse != null)
                catchBadResponse(response);
            else
                this.props.alert.error(response.statusText);
        }
    }).then(jsonBody => {
        if (typeof jsonBody !== "undefined")
            callback(jsonBody);
    }).catch(error => {
        catchError(error);
    })
}

export async function getBlobRequest(url, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url, {
        method: "GET",
        headers: new Headers({
            Accept: "application/json, text/html",
            credentials: "include",
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
        })
    }).then(response => {
        if (response.status === 200) {
            return response.blob();
        } else if (response.status === 403) {
            window.location.replace("/?status=expiredSession");
        } else {
            if (catchBadResponse != null)
                catchBadResponse(response);
            else
                this.props.alert.error(response.statusText);
        }
    }).then(blob => {
        if (typeof blob !== "undefined")
            callback(blob);
    }).catch(error => {
        catchError(error);
    })
}

export async function postRequest(url, params, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url, {
        method: "POST",
        body: JSON.stringify(params),
        headers: new Headers({
            Accept: "application/json, text/html",
            "Content-Type": "application/json",
            credentials: "include"
        })
    }).then(response => {
        if (response.status === 200) {
            callback();
        } else if (response.status === 403) {
            window.location.replace("/?status=expiredSession");
        } else {
            if (catchBadResponse != null)
                catchBadResponse(response);
            else
                this.props.alert.error(response.statusText);
        }
    }).catch(error => {
        catchError(error);
    })
}