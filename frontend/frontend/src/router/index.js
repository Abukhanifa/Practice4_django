import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Admin from '../views/Admin.vue';
import Register from '../views/Register.vue';
import store from '../store';

const routes = [
    { path: '/', component: Login },
    { 
        path: '/admin',
        component: Admin,
        meta: { requiresAdmin: true } 
    },
    { path: '/register', component: Register }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        try {
            if (!store.state.user) {
                await store.dispatch('fetchUser');  // Fetch user only if not already available
            }
            if (store.state.user?.role === 'admin') {
                next();
            } else {
                next('/'); // Redirect if not admin
            }
        } catch (error) {
            console.error("User authentication failed:", error);
            next('/'); // Redirect if there's an error fetching the user
        }
    } else {
        next();
    }
});

export default router;
