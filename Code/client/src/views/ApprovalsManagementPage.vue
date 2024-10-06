<template>
    <NavBar></NavBar>
    <ApprovalsManagement :key="refreshKey" @approvalUpdated="refreshCategoryManagement"></ApprovalsManagement>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import ApprovalsManagement from '@/components/ApprovalsManagement.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    ApprovalsManagement
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