import {create} from 'zustand';
import {mountStoreDevtool} from 'simple-zustand-devtools';

export const useAuthStore = create((set, get) => ({
    alluserdata: null,
    loading: false,

    user: () => ({
        user_id: get().alluserdata?.user_id || null,
        username: get().alluserdata?.username || null,
    }),

    setUser: (user) => set({
        alluserdata: user,
    }),

    setLoading: (loading) => set({loading}),

    logout: () => set({
        alluserdata: null,
    }),

    isLoggedIn: () => get().alluserdata !== null,

}));

if (import.meta.env.MODE === 'development') {
    mountStoreDevtool('AuthStore', useAuthStore);
}

