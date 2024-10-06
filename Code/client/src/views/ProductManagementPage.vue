<template>
    <NavBar></NavBar>
    <ProductManagement :key="refreshKey" @productDeleted="refreshProductManagement"></ProductManagement>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import ProductManagement from '@/components/Product/ProductManagement.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    ProductManagement
  },
  data() {
    return {
      refreshKey: 0, // Initial key value
    };
  },
  methods: {
    refreshProductManagement(productId) {
      console.log('Refreshing product list',productId)
      // Logic to refresh the product list
      // You can fetch the updated product list or update the existing list in the component state
       this.refreshKey += 1;
    },
  },
};
</script>