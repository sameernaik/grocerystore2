<template>
  <h6 v-if="isAdmin" style="color: #E91E63;text-align: left;margin-left:50px"> Welcome, Admin !</h6>
  <h6 v-if="isStoreManager && !isAdmin" style="color: #E91E63;text-align: left;margin-left:50px"> Welcome, Store Manager !</h6>
  <h6 v-if="isUser && !isStoreManager && !isAdmin" style="color: #E91E63;text-align: left;margin-left:50px"> Welcome, User!</h6>
  <nav>
    <div class="large-font">
    <ul>
    <img src="@/assets/img/logo-png.png" :width="160" :height="50">
    <router-link v-if="isAdmin" to="/admin">Admin</router-link>
    <template v-if="isStoreManager">
    <router-link to="/summary">Summary</router-link>
    <router-link to="/category">Category</router-link>
    <router-link to="/product">Product</router-link>
    <!--<router-link to="/messages">Messages</router-link>-->
    </template>
     
    <!--<li>
        <input type="text" placeholder="Search" v-model="searchQuery" @input="handleSearch" style="width: 500px; margin: 0 auto;"/>
      </li>-->
      <!--
      <div class="card card-body" style="margin: 0; padding: 0; max-width: 500px;background-color: #fef4f8">
    <div class="row">
      <form
        id="search-form"
        class="d-flex"
        action="/search"
        method="post"
        style="max-width: 880px;"
      >
        <select
          name="category-id"
          id="category-id"
          class="form-control"
          style="font-size: 1rem; margin-left: 5px; margin-top: 10px; width: 140px; background-color: #fef4f8; color: #E91E63;"
          required
        >
          <option value="0" :selected="searchedCategoryId === 0">Any Category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id" :selected="searchedCategoryId === category.id">
            {{ category.name }}
          </option>
        </select>

        <input 
              type="text"
              v-model="searchedProductName"
              name="search-input"
              class="form-control"
              style="margin-left: 5px; margin-top: 10px; width: 430px; font-size: 1rem;"
              placeholder="Search Product Name">
              
        <a @click="search" style="border-color: lightgrey; margin-right: 0; margin-top: 10px; padding: 5px; color: #E91E63; font-size: 1rem; font-weight: 500" class="btn me-3">
        Search
        </a>

      </form>
      <div >
     <router-link to="/advanced-search" style="margin-left: 200px; padding-top: 5px; color: #E91E63; font-size: 0.7rem; font-weight: 500;background-color: #fef4f8">Advanced Search</router-link>
      
    </div>
    </div>
    </div>-->
      <router-link to="/advanced-search">Search</router-link>
      <router-link to="/shop">Shop</router-link>
      <router-link v-if="!isUser" to="/login">Login</router-link>
      <template v-if="isUser">
      <router-link to="/past-order">My Orders</router-link>
      <router-link to="/cart">My Cart&nbsp;&nbsp;<i class="fa fa-shopping-basket"></i>&nbsp;{{ totalQuantity }}</router-link>
      
      <!-- Add a logout link -->
      <a v-if="isUser || isStoreManager || isAdmin" @click="logout" style="cursor: pointer;color: #E91E63">
        Logout
      </a>
    
    </template>
    </ul>
    </div>
   
     
  </nav>
</template>

<script setup>
//import { mapGetters } from 'vuex';
import { useRouter } from 'vue-router';
import { computed, onMounted } from 'vue';
import {useStore} from 'vuex';

const router = useRouter();
//import { useRouter } from 'vue-router';
const store = useStore();

/*const router = useRouter();
const searchedProductName = ref('');
const search = async () => {
  console.log("NavBar.vue searchedProductName.value ",searchedProductName.value)
   store.dispatch('filterProductsByName',searchedProductName.value);
   router.push('/search-result');
};*/
  
const isAdmin = computed (() => localStorage.getItem('isAdmin') === 'true' || false);
const isStoreManager = computed (() => localStorage.getItem('isStoreManager') === 'true' || false);
const isUser = computed (() => localStorage.getItem('isUser') === 'true' || false);


//const { getTotalQuantity }  = mapGetters(['getTotalQuantity']);
const totalQuantity = computed (() => store.state.totalQuantity);


onMounted(async () => {
//totalQuantity.value = store.getters.getTotalQuantity;
console.log('onMounted NavBar totalQuantity',totalQuantity.value );
});

  const logout = () => {
   store.dispatch('logout');
   router.push('/login');
};


</script>

<style scoped>
 @import '@/assets/css/theme.css';
 @import '@/assets/fonts/font-awesome/font-awesome.css';
nav {
  padding: 1px;
}

ul {
  list-style: none;
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
}

router-link {
  background-color: #fad1df; 
  color: #E91E63;
  padding: 1px;
  border-radius: 5px;
}

router-link:hover {
  background-color: #fad1df;
}
.large-font {
    font-size: 18px; /* Adjust the font size as needed */
    font-weight: bold;
    border: 2px solid #333; 
    padding: 1px;
    border-color:  #E91E63;
    background-color: #fad1df;
  }
a{
  background-color: #fad1df; 
  color: #E91E63;
  padding: 7px;
}
</style>
