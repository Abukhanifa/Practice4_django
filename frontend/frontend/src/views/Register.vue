<!-- eslint-disable vue/multi-word-component-names -->
<template> 

  <v-container> 

    <v-card class="mx-auto pa-4" max-width="400"> 

      <v-card-title>Register</v-card-title> 

      <v-card-text> 

        <v-form @submit.prevent="register"> 

          <v-text-field v-model="username" label="Username" required></v-text-field> 

          <v-text-field v-model="email" label="Email" required></v-text-field> 

          <v-select v-model="role" :items="roles" label="Role" required></v-select> 

          <v-text-field v-model="password" label="Password" type="password" required></v-text-field> 

          <v-text-field v-model="password2" label="Confirm Password" type="password" required></v-text-field> 

          <v-btn color="primary" type="submit" block>Register</v-btn> 

        </v-form> 

      </v-card-text> 

    </v-card> 

  </v-container> 

</template> 

 

<script> 

import axios from 'axios'; 

 

export default { 

  data() { 

    return { 

      username: '', 

      email: '', 

      role: 'user', 

      roles: ['user', 'admin'], 

      password: '', 

      password2: '', 

    }; 

  }, 

  methods: { 

    async register() { 

      try { 

        await axios.post('http://127.0.0.1:8000/api/register/', { 

          username: this.username, 

          email: this.email, 

          role: this.role, 

          password: this.password, 

          password2: this.password2, 

        }); 

        this.$router.push('/'); 

      } catch (error) { 

        console.error(error); 

      } 

    }, 

  }, 

}; 

</script>