<template>
    <NavBar></NavBar>
    <SearchResultPanel></SearchResultPanel>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import SearchResultPanel from '@/components/SearchResultPanel.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    SearchResultPanel
  }
}
</script>