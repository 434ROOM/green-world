import axios from "axios";
import serverConfig from "./serverConfig";
import { message } from "ant-design-vue";
import router from "./router";

function hasToken() {
    return localStorage.getItem("access_token") != null && localStorage.getItem("refresh_token") != null;
}

function getAccessToken() {
    if (isVaildAccessToken()) {
        return localStorage.getItem("access_token");
    }
    else {
        refreshToken();
        return localStorage.getItem("access_token");
    }
}

function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

function setAccessToken(token) {
    localStorage.setItem("access_token", token);
}

function setRefreshToken(token) {
    localStorage.setItem("refresh_token", token);
}

// JWT token decode
const decodeJwt = (token) => {
    const parts = token.split('.');
    if (parts.length !== 3) {
        throw new Error('Invalid JWT token format');
    }

    const decodedHeader = JSON.parse(atob(parts[0]));
    const decodedPayload = JSON.parse(atob(parts[1]));

    return {
        header: decodedHeader,
        payload: decodedPayload,
        signature: parts[2] // 签名部分，通常在前端不做处理
    };
};

function isVaildRefreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    const decoded_refresh_token = refresh_token ? decodeJwt(refresh_token) : null;
    if (decoded_refresh_token == null) {
        return false;
    }
    const isRefreshTokenExpired = refresh_token ? (Date.now() >= decoded_refresh_token.payload.exp * 1000) : true;
    return !isRefreshTokenExpired;
}

function isVaildAccessToken() {
    const access_token = localStorage.getItem("access_token");
    const decoded_access_token = access_token ? decodeJwt(access_token) : null;
    if (decoded_access_token == null) {
        return false;
    }
    const isAccessTokenExpired = access_token ? (Date.now() >= decoded_access_token.payload.exp * 1000) : true;
    return !isAccessTokenExpired;
}

function refreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    const formData = new FormData();
    formData.append('refresh', refresh_token);
    if (isVaildRefreshToken()) {
        const headers = {
            "Content-Type": "multipart/form-data",
        };
        axios.post(serverConfig.apiUrl + '/login/refresh', formData, { headers: headers })
            .then(response => {
                const new_access_token = response.data.access;
                setAccessToken(new_access_token);
            })
            .catch(error => {
                console.log(error);
                message.error("刷新 token 失败，请重新登录");
                router.push({ path: '/login' });
            })
    }
    else {
        console.error("refresh token is expired");
        message.error("登录过期，请重新登录");
        router.push({ path: '/login' });
    }
}

function getUsername() {
    const access_token = localStorage.getItem("access_token");
    const decoded_access_token = access_token ? decodeJwt(access_token) : null;
    if (decoded_access_token == null) {
        return null;
    }
    return decoded_access_token.payload.username;
}

function getEmail() {
    const access_token = localStorage.getItem("access_token");
    const decoded_access_token = access_token ? decodeJwt(access_token) : null;
    if (decoded_access_token == null) {
        return null;
    }
    return decoded_access_token.payload.email;
}

function getUserId() {
    const access_token = localStorage.getItem("access_token");
    const decoded_access_token = access_token ? decodeJwt(access_token) : null;
    if (decoded_access_token == null) {
        return null;
    }
    return decoded_access_token.payload.user_id;
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

export default {
    hasToken,
    getAccessToken,
    getRefreshToken,
    setAccessToken,
    setRefreshToken,
    decodeJwt,
    isVaildRefreshToken,
    isVaildAccessToken,
    refreshToken,
    getUsername,
    getEmail,
    getUserId,
    logout
};
