<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    ...mapActions(['login']),

    async handleLogin() {
      try {
        console.log("Attempting to login...");  // Debugging
        await this.login({ username: this.username, password: this.password });
        console.log("Login successful! Redirecting...");
        this.$router.push('/admin');
      } catch (error) {
        console.error("Login failed:", error);  // Catch errors
        alert("Login failed! Check console.");
      }
    },
  },
};
</script>
