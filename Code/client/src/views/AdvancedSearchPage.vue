<template>
    <NavBar></NavBar>
    <AdvancedSearch></AdvancedSearch>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import AdvancedSearch from '@/components/AdvancedSearch.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    AdvancedSearch
  }
}
</script>