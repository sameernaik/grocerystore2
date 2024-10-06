<template>
    <NavBar></NavBar>
    <ProductCategory></ProductCategory>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import ProductCategory from '@/components/Product/ProductCategory.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    ProductCategory
  }
}
</script>