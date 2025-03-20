<!-- eslint-disable vue/multi-word-component-names -->
<template> 
  <v-container> 
    <v-card> 
      <v-card-title>Admin Panel</v-card-title> 
      <v-btn color="red" @click="logout" class="ma-2">Logout</v-btn> 
      <v-table> 
        <thead> 
          <tr> 
            <th>Name</th> 
            <th>Description</th> 
            <th>Actions</th> 
          </tr> 
        </thead> 
        <tbody> 
          <tr v-for="item in items" :key="item.id"> 
            <td>{{ item.name }}</td> 
            <td>{{ item.description }}</td> 
            <td> 
              <v-btn color="red" @click="deleteItem(item.id)">Delete</v-btn> 
            </td> 
          </tr> 
        </tbody> 
      </v-table> 
    </v-card> 
  </v-container> 
</template> 

<script> 
import { mapState } from 'vuex'; 
import axios from 'axios'; 

export default { 
  data() { 
    return { items: [] }; 
  }, 
  computed: { 
    ...mapState(['token']), 
  }, 
  async created() { 
    try { 
      const response = await axios.get('http://127.0.0.1:8000/api/items/', { 
        headers: { Authorization: `Bearer ${this.token}` }, 
      }); 
      this.items = response.data; 
    } catch (error) { 
      console.error('Error fetching items:', error); 
    } 
  }, 
  methods: {
    async logout() {
        try {
            const refreshToken = localStorage.getItem("refresh_token");

            if (!refreshToken) {
                console.error("No refresh token found.");
                return;
            }

            const response = await axios.post(
                "http://127.0.0.1:8000/api/logout/",
                { refresh: refreshToken },  // Send refresh token in the request body
                { headers: { Authorization: `Bearer ${this.token}` } }
            );

            console.log("Logout response:", response.data);

            // Clear tokens and redirect
            this.$store.commit("SET_TOKEN", null);
            localStorage.removeItem("token");
            localStorage.removeItem("refresh_token");
            this.$router.push("/");
        } catch (error) {
            console.error("Logout failed:", error.response?.data || error.message);
        }
    
    },

    async deleteItem(id) { 
      try { 
        await axios.delete(`http://127.0.0.1:8000/api/items/${id}/`, { 
          headers: { Authorization: `Bearer ${this.token}` }, 
        }); 
        this.items = this.items.filter(item => item.id !== id); 
      } catch (error) { 
        console.error('Error deleting item:', error); 
      } 
    }, 
  }
}

</script>
