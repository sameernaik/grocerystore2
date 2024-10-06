<template>
    <NavBar></NavBar>
    <CheckoutPanel></CheckoutPanel>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import CheckoutPanel from '@/components/CheckoutPanel.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    CheckoutPanel
  }
}
</script>