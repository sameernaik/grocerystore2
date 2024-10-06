<template>
    <NavBar></NavBar>
    <CartList></CartList>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import CartList from '@/components/CartList.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    CartList
  }
}
</script>