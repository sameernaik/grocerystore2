<template>
    <NavBar></NavBar>
    <SummaryPanel></SummaryPanel>
</template>

<script>
import NavBar from '@/layouts/NavBar.vue'
import SummaryPanel from '@/components/SummaryPanel.vue'


export default {
    name: 'App',
    components: {
        NavBar,
        SummaryPanel
    },
    
};
</script>