import { createStore } from 'vuex';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

export default createStore({
    state: {
        user: null,
        token: localStorage.getItem('token') || '',
    },

    mutations: {
        SET_USER(state, user) {
            state.user = user;
        },

        SET_TOKEN(state, token) {
            state.token = token;
            localStorage.setItem('token', token);
        },

        LOGOUT(state) {
            state.user = null;
            state.token = '';
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');  // Make sure to remove the refresh token as well
        },
    },

    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await axios.post(`${API_URL}login/`, credentials);
                
                console.log("Login response:", response.data); // Проверка, что токены приходят
                
                commit('SET_TOKEN', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh); // Сохраняем refresh-токен
                await this.dispatch('fetchUser');  // Загружаем данные пользователя
            } catch (error) {
                console.error("Login failed:", error.response?.data || error.message);
                throw error;  // Позволит обработать ошибку в UI
            }
        },

        async fetchUser({ commit, state }) {
            if (!state.token) return; // Avoid making requests if no token

            try {
                const response = await axios.get(`${API_URL}user/`, {
                    headers: { Authorization: `Bearer ${state.token}` }
                });
                commit('SET_USER', response.data);
            } catch (error) {
                console.error("Error fetching user:", error.response?.data || error.message);

                if (error.response?.status === 401) {
                    this.dispatch('logout');  // Logout if token is invalid
                }
            }
        },

        async logout({ commit }) {
            try {
                const refreshToken = localStorage.getItem("refresh_token");
        
                console.log("Sending Refresh Token:", refreshToken);  // Debugging
        
                if (!refreshToken) {
                    console.error("No refresh token found.");
                    return;
                }
        
                const response = await axios.post(
                    `${API_URL}logout/`, 
                    { refresh: refreshToken },  // Must match Django expected data
                    { 
                        headers: { 
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${this.state.token}`
                        }
                    }
                );
        
                console.log("Logout response:", response.data); // Debug response
        
                localStorage.removeItem("token");
                localStorage.removeItem("refresh_token");
                commit('LOGOUT');
            } catch (error) {
                console.error("Logout request failed:", error.response?.data || error.message);
            }
        }
        
        
    },
});
