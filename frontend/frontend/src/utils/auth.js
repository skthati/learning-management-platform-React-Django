import {useAuthStore} from '../store/auth';
import {axios} from './axios';
import jwtDecode from 'jwt-decode';
import cookie from 'js-cookie';
import Swal from 'sweetalert2';

export const login = async (email, password) => {
    try {
        const {data, status} = await axios.post('user/token/', {email, password});

        if (status === 200) {
            setAuthUser(data.access, data.refresh);
            alert('Login successful');
        }

        return {data, error: null};
    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.response.data?.detail || "Something went wrong",
        });
        return {data: null, error: error.response.data?.detail || "Something went wrong"};
    }
};

export const register = async (full_name, email, password1, password2) => {
    try {
        const {data, status} = await axios.post('user/register/', {full_name, email, password1, password2});

        if (status === 201) {
            await login(email, password1);
            alert('Registration successful');
        }

        return {data, error: null};
    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.response.data?.detail || "Something went wrong",
        });
        return {data: null, error: error.response.data?.detail || "Something went wrong"};
    }
}


export const logout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    useAuthStore.getState().setUser(null);
    alert('Logout successful');
}

export const setUser = async () => {
    const access_token = Cookies.get('access_token');
    const refresh_token = Cookies.get('refresh_token');

    if (!access_token || !refresh_token) {
        return;
    }

    if (isAccessTokenExpired(access_token)) {
        const {data, error} = await getRefreshAccessToken(refresh_token);
        if (error) {
            return;
        }
        setAuthUser(data.access, data.refresh);
    } else {
        setAuthUser(access_token, refresh_token);
    }
}

export const setAuthUser = (access_token, refresh_token) => {
    Cookies.set('access_token', access_token, {expires: 1, secure: true});
    Cookies.set('refresh_token', refresh_token, {expires: 1, secure: true});

    const user = jwtDecode(access_token) ?? null;

    if (user) {
        useAuthStore.getState().setUser(user);
    } else {
        useAuthStore.getState().setLoading(false);
    }
}

export const getRefreshAccessToken = async () => {
    try {
        const refresh_token = Cookies.get('refresh_token');
        const {data, status} = await axios.post('user/token/refresh/', {refresh: refresh_token});

        if (status === 200) {
            return {data, error: null};
        }
    } catch (error) {
        console.error(error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.response.data?.detail || "Something went wrong",
        });
        return {data: null, error: error.response.data?.detail || "Something went wrong"};
    }
}

export const isAccessTokenExpired = (access_token) => {
    try {
        const decodedtoken = jwtDecode(access_token);
        return decodedtoken.exp < Date.now() / 1000;
    } catch (error) {
        console.error('Invalid token:', error.message);
        throw new Error('Failed to decode token');
        return true;
    }
};