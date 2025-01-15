import axios  from "axios";
import { API_URL } from "./constants";
import { getRefreshAccessToken, isAccessTokenExpired, setAuthUser } from "./auth";
import Cookies from "js-cookie";

const useAxios = () => {
    const access_token = Cookies.get("access_token");
    const refresh_token = Cookies.get("refresh_token");

    const axiosInstance = axios.create({
        baseURL: API_URL,
        timeout: 10000,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${access_token}`,
        },
    });

    axiosInstance.interceptors.request.use(async (config) => {
        if (!isAccessTokenExpired()) {
            return config;
        } else {
            const new_access_token = await getRefreshAccessToken(refresh_token);
            setAuthUser(new_access_token.access, new_access_token.refresh);
            config.headers['Authorization'] = `Bearer ${new_access_token.access}`;
            return config;
        }
        return axiosInstance;
    });

};

export default useAxios;

