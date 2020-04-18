import { getApiURL } from "./env";


export async function getRequest(url, token, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url + (token === "demo" ? "?demo=1" : ""), {
        method: "GET",
        headers: new Headers({
            "X-Authorization": "Bearer " + token,
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

export async function getBlobRequest(url, token, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url + (token === "demo" ? "?demo=1" : ""), {
        method: "GET",
        headers: new Headers({
            "X-Authorization": "Bearer " + token,
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

export async function postRequest(url, token, params, callback, catchBadResponse, catchError) {
    fetch(getApiURL() + url, {
        method: "POST",
        body: JSON.stringify(params),
        headers: new Headers({
            "X-Authorization": "Bearer " + token,
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

export async function getForeignRequest(url, callback, catchBadResponse, catchError) {
    fetch(url, {
        method: "GET",
        mode: 'cors',
        headers: {
            "Accept": "application/json, text/html",
            "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, " +
                "Origin,Accept, " +
                "X-Requested-With, " +
                "Content-Type, " +
                "Access-Control-Request-Method, " +
                "Access-Control-Request-Headers, " +
                "Access-Control-Allow-Origin, " +
                "Access-Control-Allow-Credentials",
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "GET,OPTIONS,HEAD",
            "Access-Control-Allow-Credentials": "true",
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
        }
    }).then(response => {
        if (response.status === 200) {
            return response.json();
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

export function saveAnalytics(token, event) {
    let params = {"event": event, "demo_user": token.startsWith("demo") ? token : undefined}
    postRequest.call(this, "analytics/save", token, params, () => {}, () => {
        console.log("Error while saving the pageanalytics");
    }, () => {
        console.log("Error while saving the pageanalytics");
    });
}