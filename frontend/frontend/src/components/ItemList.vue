<template> 

  <div> 

    <h1>Items</h1> 

    <ul> 

      <li v-for="item in items" :key="item.id"> 

        {{ item.name }} - {{ item.description }} 

      </li> 

    </ul> 

    <form @submit.prevent="addItem"> 

      <input v-model="newItem.name" placeholder="Name" required /> 

      <input v-model="newItem.description" placeholder="Description" required /> 

      <button type="submit">Add Item</button> 

    </form> 

  </div> 

</template> 

 

<script> 

import { getItems, createItem } from '../api'; 

 

export default { 

  data() { 

    return { 

      items: [], 

      newItem: { name: '', description: '' }, 

    }; 

  }, 

  async created() { 

    this.items = await getItems(); 

  }, 

  methods: { 

    async addItem() { 

      const item = await createItem(this.newItem); 

      this.items.push(item); 

      this.newItem = { name: '', description: '' }; 

    }, 

  }, 

}; 

</script> 