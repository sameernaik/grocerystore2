<template>
    <NavBar></NavBar>
    <OrderConfirmationPanel></OrderConfirmationPanel>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import OrderConfirmationPanel from '@/components/OrderConfirmationPanel.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    OrderConfirmationPanel
  }
}
</script>