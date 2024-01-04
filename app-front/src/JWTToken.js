import axios from "axios";

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

function setAccessToken(token) {
    localStorage.setItem("access_token", token);
}

function refreshToken() {
    const access_token = getAccessToken();
    const refresh_token = getRefreshToken();
    if (access_token && refresh_token) {
        const payload = {
            "refresh_token": refresh_token
        };
        const headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        };
        axios.post("http://localhost:8000/api/token/refresh/", payload, {headers: headers})
            .then(response => {
                setAccessToken(response.data.access);
            })
            .catch(error => {
                console.log(error);
            })
    }
}
