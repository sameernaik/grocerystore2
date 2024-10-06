<template>
<!--<LoginForm1 />-->
<!--<NavBar />-->
<!--<AdvancedSearch />-->
<div id='app'>
  <router-view />
</div>


</template>

<script>
//import LoginForm1 from './components/LoginForm1.vue'
//import NavBar from "@/layouts/NavBar.vue";
//import AdvancedSearch from "@/components/AdvancedSearchBar.vue";

export default {
  name: 'App',
  components: {
    //AdvancedSearch
    //LoginForm1
   // NavBar
  },
   mounted() {
                  document.title = "Gurukrupa Grocery Store";
                      },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  margin-top: 60px;
}
</style> 
