<template>
    <NavBar></NavBar>
    <OrderHistoryPanel></OrderHistoryPanel>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import OrderHistoryPanel from '@/components/OrderHistoryPanel.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    OrderHistoryPanel
  }
}
</script>