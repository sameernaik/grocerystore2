<template>
    <NavBar></NavBar>
    <CategoryManagement :key="refreshKey" @categoryDeleted="refreshCategoryManagement"></CategoryManagement>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import CategoryManagement from '@/components/CategoryManagement.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    CategoryManagement
  },
  data() {
    return {
      refreshKey: 0, // Initial key value
    };
  },
  methods: {
    refreshCategoryManagement(categoryId) {
      console.log('Refreshing category list', categoryId)
      // Logic to refresh the product list
      // You can fetch the updated product list or update the existing list in the component state
      this.refreshKey += 1;
    },
  },
};
</script>